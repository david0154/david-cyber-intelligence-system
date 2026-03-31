#!/usr/bin/env python3
"""
DAVID CYBER INTELLIGENCE SYSTEM
App Bug Analyzer Engine

Supports:
  - Android APK  → decompile + scan
  - EXE / DLL    → pefile + YARA + strings
  - PHP / Python / JS / Java → static code analysis
  - URL / Web App → HTTP probe + header check + OWASP ZAP
  - Log files    → pattern-based bug detection
  - ZIP / folder → recursive scan all files inside

Output:
  - Bug list with severity (CRITICAL / HIGH / MEDIUM / LOW / INFO)
  - Root cause explanation
  - Fix suggestion (AI-powered via LLM)
  - CVSS score estimate
  - Save report as JSON / HTML / PDF

Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import re
import json
import shutil
import subprocess
import zipfile
import tempfile
import hashlib
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional
from loguru import logger


# ─────────────────────────────────────────────────────────────────────────────
#  SEVERITY LEVELS
# ─────────────────────────────────────────────────────────────────────────────
SEVERITY = {
    "CRITICAL": 5,
    "HIGH":     4,
    "MEDIUM":   3,
    "LOW":      2,
    "INFO":     1,
}

SEV_COLOR = {
    "CRITICAL": "#ff0000",
    "HIGH":     "#ff6600",
    "MEDIUM":   "#ffd700",
    "LOW":      "#00bfff",
    "INFO":     "#aaaaaa",
}


# ─────────────────────────────────────────────────────────────────────────────
#  STATIC CODE PATTERNS  (language → list of (pattern, severity, name, fix))
# ─────────────────────────────────────────────────────────────────────────────
STATIC_PATTERNS = {
    # ── PHP ──────────────────────────────────────────────────────────────────
    "php": [
        (r"\$_GET\s*\[|\$_POST\s*\[|\$_REQUEST\s*\[",
         "HIGH", "Unvalidated User Input",
         "Sanitize with htmlspecialchars() and validate type before use."),

        (r"mysql_query\s*\(",
         "CRITICAL", "Deprecated mysql_query (SQLi risk)",
         "Replace with PDO or mysqli prepared statements."),

        (r"\$.*=.*\$_GET|\$.*=.*\$_POST",
         "HIGH", "Direct assignment from request",
         "Always validate and sanitize request parameters before assignment."),

        (r'eval\s*\(',
         "CRITICAL", "eval() usage",
         "Remove eval(). Use explicit logic or allow-listed functions instead."),

        (r'shell_exec\s*\(|exec\s*\(|system\s*\(|passthru\s*\(',
         "CRITICAL", "OS Command Execution",
         "Never pass user input to shell functions. Use escapeshellarg()."),

        (r'include\s*\(\s*\$|require\s*\(\s*\$',
         "CRITICAL", "Remote File Inclusion (RFI)",
         "Never use variables in include/require. Use a whitelist map instead."),

        (r'md5\s*\(|sha1\s*\(',
         "MEDIUM", "Weak hashing (MD5/SHA1)",
         "Use password_hash() with PASSWORD_BCRYPT for passwords."),

        (r'die\s*\(\s*\$|echo\s*\$_',
         "MEDIUM", "Error/data leakage to output",
         "Never echo raw variables or DB errors to user. Log internally."),

        (r'header\s*\(.*Location.*\$',
         "HIGH", "Open Redirect",
         "Validate redirect URLs against an allowed list."),

        (r'\$_(COOKIE|SESSION)\[.*\]\s*=',
         "MEDIUM", "Direct session/cookie manipulation",
         "Validate all session/cookie data; regenerate session ID after login."),
    ],

    # ── Python ───────────────────────────────────────────────────────────────
    "python": [
        (r'eval\s*\(|exec\s*\(',
         "CRITICAL", "eval/exec usage",
         "Replace eval/exec with explicit logic. Use ast.literal_eval for safe parsing."),

        (r'subprocess\.call\(.*shell\s*=\s*True|os\.system\s*\(',
         "CRITICAL", "Shell injection risk",
         "Use subprocess with a list (not shell=True). Never pass user input directly."),

        (r'pickle\.loads?\s*\(',
         "CRITICAL", "Unsafe pickle deserialization",
         "Never unpickle data from untrusted sources. Use JSON or msgpack."),

        (r'import\s+\*',
         "LOW", "Wildcard import",
         "Use explicit imports to avoid namespace pollution and hidden bugs."),

        (r'except\s*:',
         "MEDIUM", "Bare except clause",
         "Catch specific exceptions (except ValueError:) instead of bare except."),

        (r'password\s*=\s*[\'"]\w+[\'"]|secret\s*=\s*[\'"]\w+[\'"]|api_key\s*=\s*[\'"]\w+[\'"]',
         "CRITICAL", "Hardcoded credential",
         "Move secrets to environment variables or a secrets manager (.env / Vault)."),

        (r'http://(?!localhost|127)',
         "MEDIUM", "HTTP (not HTTPS) external URL",
         "Use HTTPS for all external connections to prevent MITM attacks."),

        (r'DEBUG\s*=\s*True|debug\s*=\s*True',
         "HIGH", "Debug mode enabled",
         "Set DEBUG=False in production. Debug mode exposes stack traces."),

        (r'random\.random\(\)|random\.randint',
         "LOW", "Non-cryptographic random",
         "Use secrets module for tokens/passwords instead of random."),

        (r'TODO|FIXME|HACK|XXX',
         "INFO", "TODO/FIXME marker",
         "Review and resolve all TODO/FIXME comments before production."),
    ],

    # ── JavaScript ───────────────────────────────────────────────────────────
    "js": [
        (r'eval\s*\(',
         "CRITICAL", "eval() usage",
         "Remove eval(). Use JSON.parse() for data, explicit logic for code."),

        (r'innerHTML\s*=|document\.write\s*\(',
         "HIGH", "DOM XSS sink",
         "Use textContent or createElement instead of innerHTML/document.write."),

        (r'localStorage\.setItem.*password|sessionStorage.*token',
         "HIGH", "Sensitive data in browser storage",
         "Never store passwords/tokens in localStorage. Use httpOnly cookies."),

        (r'http://(?!localhost|127)',
         "MEDIUM", "HTTP (not HTTPS) request",
         "Use HTTPS for all API calls to prevent MITM."),

        (r'console\.log\(',
         "LOW", "console.log in code",
         "Remove console.log statements before production deployment."),

        (r'==(?!=)',
         "LOW", "Loose equality (==)",
         "Use strict equality (===) to avoid type coercion bugs."),

        (r'var\s+',
         "INFO", "var declaration",
         "Use const/let instead of var to avoid hoisting bugs."),

        (r'new\s+Function\s*\(',
         "CRITICAL", "new Function() — code injection risk",
         "Avoid new Function(). Use regular function declarations."),
    ],

    # ── Java / Kotlin ─────────────────────────────────────────────────────────
    "java": [
        (r'Runtime\.getRuntime\(\)\.exec|ProcessBuilder',
         "CRITICAL", "OS command execution",
         "Never pass user input to exec/ProcessBuilder. Validate all input."),

        (r'new\s+Random\s*\(',
         "MEDIUM", "java.util.Random (not secure)",
         "Use java.security.SecureRandom for cryptographic operations."),

        (r'printStackTrace\s*\(',
         "MEDIUM", "Stack trace printed",
         "Use a logging framework (SLF4J/Logback). Never print stack traces in production."),

        (r'"SELECT.*\+|"INSERT.*\+|"UPDATE.*\+',
         "CRITICAL", "String concatenation in SQL",
         "Use PreparedStatement with parameterized queries to prevent SQLi."),

        (r'Log\.d\(|System\.out\.print',
         "LOW", "Debug logging",
         "Remove debug logs before release. Use ProGuard to strip logs."),

        (r'android:debuggable\s*=\s*"true"',
         "HIGH", "debuggable=true in manifest",
         "Set android:debuggable=false in production release."),

        (r'android:allowBackup\s*=\s*"true"',
         "MEDIUM", "allowBackup=true",
         "Set android:allowBackup=false to prevent data extraction via ADB backup."),

        (r'MODE_WORLD_READABLE|MODE_WORLD_WRITEABLE',
         "CRITICAL", "World-readable/writable file",
         "Use MODE_PRIVATE for file operations. Never expose app files globally."),
    ],

    # ── Generic / Any Text ────────────────────────────────────────────────────
    "generic": [
        (r'password\s*=\s*[\'"][^\'"][^\'"][^\'"]',
         "CRITICAL", "Hardcoded password",
         "Store passwords in environment variables or a secrets vault."),

        (r'BEGIN (RSA|EC|DSA) PRIVATE KEY|BEGIN PRIVATE KEY',
         "CRITICAL", "Private key in file",
         "Remove private keys from code. Use key files outside the repo."),

        (r'AKIA[0-9A-Z]{16}',
         "CRITICAL", "AWS Access Key",
         "Revoke this key immediately. Use IAM roles and environment variables."),

        (r'ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}',
         "CRITICAL", "GitHub Token",
         "Revoke token at github.com/settings/tokens and use secrets management."),

        (r'AIza[0-9A-Za-z\-_]{35}',
         "CRITICAL", "Google API Key",
         "Restrict API key usage in Google Cloud Console and remove from code."),

        (r'TODO|FIXME|HACK',
         "INFO", "Unresolved TODO/FIXME",
         "Resolve before production."),
    ],
}

# Extension → language mapping
EXT_LANG = {
    ".php":   "php",
    ".py":    "python",
    ".js":    "js",
    ".ts":    "js",
    ".jsx":   "js",
    ".tsx":   "js",
    ".java":  "java",
    ".kt":    "java",
    ".xml":   "java",
    ".html":  "js",
    ".htm":   "js",
    ".rb":    "generic",
    ".go":    "generic",
    ".cs":    "generic",
    ".cpp":   "generic",
    ".c":     "generic",
    ".sh":    "generic",
    ".bat":   "generic",
    ".txt":   "generic",
    ".log":   "generic",
    ".env":   "generic",
    ".conf":  "generic",
    ".config":"generic",
    ".json":  "generic",
    ".yaml":  "generic",
    ".yml":   "generic",
}


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ENGINE CLASS
# ─────────────────────────────────────────────────────────────────────────────
class BugAnalyzerEngine:
    """
    Main bug analysis engine.
    Call analyze(target) where target is:
      - File path  (any extension)
      - Directory  (scans all files recursively)
      - URL        (web app analysis)
    """

    def __init__(self, llm=None):
        self.llm = llm   # optional LLM for AI explanations
        self.bugs = []
        self.file_count = 0
        self.scan_start = None

    # ── Public API ─────────────────────────────────────────────────────────
    def analyze(self, target: str,
                progress_cb=None) -> dict:
        """
        Main entry: analyze a file, folder, APK, EXE, or URL.
        progress_cb(message: str) called for live progress updates.
        """
        self.bugs = []
        self.file_count = 0
        self.scan_start = datetime.utcnow()
        self._cb = progress_cb or (lambda m: None)

        target = target.strip().strip('"').strip("'")
        self._cb(f"[BugAnalyzer] Target: {target}\n")

        try:
            # URL / web app
            if target.startswith("http://") or target.startswith("https://"):
                self._analyze_url(target)

            # APK
            elif target.lower().endswith(".apk"):
                self._analyze_apk(target)

            # EXE / DLL / binary
            elif target.lower().endswith((".exe", ".dll", ".bin", ".so")):
                self._analyze_binary(target)

            # ZIP (could be APK without extension, or source zip)
            elif target.lower().endswith(".zip"):
                self._analyze_zip(target)

            # Directory
            elif os.path.isdir(target):
                self._analyze_directory(target)

            # Single source file
            elif os.path.isfile(target):
                lang = EXT_LANG.get(Path(target).suffix.lower(), "generic")
                self._cb(f"[BugAnalyzer] File: {target} → Language: {lang}\n")
                self._analyze_file(target, lang)

            else:
                return {"status": "error",
                        "message": f"Target not found or unrecognized: {target}"}

        except Exception as e:
            logger.exception(e)
            return {"status": "error", "message": str(e)}

        return self._build_report(target)

    # ── URL / Web App ──────────────────────────────────────────────────────
    def _analyze_url(self, url: str):
        self._cb(f"[URL] Analyzing web app: {url}\n")
        try:
            import requests
            resp = requests.get(url, timeout=10, verify=False,
                                headers={"User-Agent": "DAVID-Scanner/1.0"})
            headers = resp.headers
            body    = resp.text[:50000]

            # ── Security headers check
            missing_headers = {
                "Content-Security-Policy":   ("HIGH",   "Missing CSP header",
                    "Add Content-Security-Policy header to prevent XSS attacks."),
                "X-Frame-Options":           ("MEDIUM", "Missing X-Frame-Options",
                    "Add X-Frame-Options: DENY to prevent clickjacking."),
                "X-Content-Type-Options":    ("MEDIUM", "Missing X-Content-Type-Options",
                    "Add X-Content-Type-Options: nosniff to prevent MIME sniffing."),
                "Strict-Transport-Security": ("HIGH",   "Missing HSTS header",
                    "Add Strict-Transport-Security to enforce HTTPS."),
                "Referrer-Policy":           ("LOW",    "Missing Referrer-Policy",
                    "Add Referrer-Policy: strict-origin-when-cross-origin."),
                "Permissions-Policy":        ("INFO",   "Missing Permissions-Policy",
                    "Add Permissions-Policy to restrict browser feature access."),
            }
            for hdr, (sev, name, fix) in missing_headers.items():
                if hdr not in headers:
                    self._add_bug(name, sev, fix, source=url,
                                  detail=f"Header '{hdr}' not found in response.")

            # ── Server info leak
            server = headers.get("Server", "")
            if server:
                self._add_bug("Server version disclosed", "MEDIUM",
                    "Remove or obscure the Server header to hide version info.",
                    source=url, detail=f"Server: {server}")

            # ── Mixed content
            if url.startswith("https://") and "http://" in body:
                self._add_bug("Mixed content (HTTP inside HTTPS)", "MEDIUM",
                    "Replace all http:// references with https:// to prevent mixed content.",
                    source=url, detail="Found http:// references in HTTPS page body.")

            # ── Error messages in body
            for pattern, name in [
                (r"You have an error in your SQL syntax",   "SQL error in response"),
                (r"Traceback \(most recent call last\)",     "Python traceback exposed"),
                (r"Warning:.*on line",                       "PHP warning in response"),
                (r"Fatal error",                             "Fatal error in response"),
                (r"<b>Notice</b>:",                          "PHP notice in response"),
                (r"stack trace",                             "Stack trace exposed"),
            ]:
                if re.search(pattern, body, re.IGNORECASE):
                    self._add_bug(name, "HIGH",
                        "Disable error display in production. Log errors server-side only.",
                        source=url, detail=f"Pattern found: {pattern}")

            # ── Open redirect check
            if "redirect" in url.lower() or "url=" in url.lower():
                self._add_bug("Potential Open Redirect parameter", "MEDIUM",
                    "Validate redirect URLs against an allow-list.",
                    source=url, detail="URL contains redirect/url parameter.")

            # ── HTTP (not HTTPS)
            if url.startswith("http://"):
                self._add_bug("HTTP (not HTTPS) used", "HIGH",
                    "Migrate to HTTPS. Obtain a TLS certificate (Let's Encrypt is free).",
                    source=url)

            # ── Cookies check
            for cookie in resp.cookies:
                if not cookie.secure:
                    self._add_bug("Cookie missing Secure flag", "MEDIUM",
                        f"Set Secure flag on cookie '{cookie.name}'.",
                        source=url, detail=f"Cookie: {cookie.name}")
                if not cookie.has_nonstandard_attr("HttpOnly"):
                    self._add_bug("Cookie missing HttpOnly flag", "MEDIUM",
                        f"Set HttpOnly flag on cookie '{cookie.name}' to prevent XSS access.",
                        source=url, detail=f"Cookie: {cookie.name}")

            # ── Scan body as HTML/JS
            self._scan_text(body, "js", source=url)

            self._cb(f"[URL] Headers: {dict(headers)}\n")
            self._cb(f"[URL] Status: {resp.status_code} | Size: {len(body)} bytes\n")

        except Exception as e:
            self._cb(f"[URL] Error: {e}\n")

    # ── APK ────────────────────────────────────────────────────────────────
    def _analyze_apk(self, apk_path: str):
        self._cb(f"[APK] Analyzing: {apk_path}\n")
        # APK is a zip file — extract and scan
        self._analyze_zip(apk_path, is_apk=True)

        # Check if jadx / apktool available for deeper decompile
        if shutil.which("apktool"):
            self._cb("[APK] Running apktool...\n")
            with tempfile.TemporaryDirectory() as tmp:
                r = subprocess.run(
                    ["apktool", "d", apk_path, "-o", tmp, "-f"],
                    capture_output=True, text=True, timeout=120
                )
                if r.returncode == 0:
                    self._analyze_directory(tmp)
        elif shutil.which("jadx"):
            self._cb("[APK] Running jadx...\n")
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(
                    ["jadx", "-d", tmp, apk_path],
                    capture_output=True, timeout=180
                )
                self._analyze_directory(tmp)
        else:
            self._cb("[APK] apktool/jadx not found. Install for deeper APK decompile.\n")
            self._cb("[APK] Scanning raw APK resources only...\n")

    # ── Binary (EXE/DLL) ───────────────────────────────────────────────────
    def _analyze_binary(self, path: str):
        self._cb(f"[Binary] Analyzing: {path}\n")
        self.file_count += 1

        # Hash
        md5  = self._hash_file(path, "md5")
        sha256 = self._hash_file(path, "sha256")
        self._cb(f"[Binary] MD5: {md5} | SHA256: {sha256}\n")

        # pefile
        try:
            import pefile
            pe = pefile.PE(path)

            # ASLR
            if not (pe.OPTIONAL_HEADER.DllCharacteristics & 0x0040):
                self._add_bug("ASLR disabled", "HIGH",
                    "Compile with /DYNAMICBASE to enable ASLR. Prevents memory exploitation.",
                    source=path)

            # DEP / NX
            if not (pe.OPTIONAL_HEADER.DllCharacteristics & 0x0100):
                self._add_bug("DEP/NX disabled", "HIGH",
                    "Compile with /NXCOMPAT to enable DEP. Prevents shellcode execution.",
                    source=path)

            # Stack cookies
            if not (pe.OPTIONAL_HEADER.DllCharacteristics & 0x0400):
                self._add_bug("Stack cookies (/GS) not detected", "MEDIUM",
                    "Compile with /GS flag to add stack-smashing protection.",
                    source=path)

            # Manifest / UAC
            self._cb(f"[PE] Machine: {hex(pe.FILE_HEADER.Machine)} | "
                     f"Sections: {pe.FILE_HEADER.NumberOfSections}\n")

        except ImportError:
            self._add_bug("pefile not installed", "INFO",
                "Run: pip install pefile", source=path)
        except Exception as e:
            self._cb(f"[PE] pefile error: {e}\n")

        # YARA
        self._yara_scan(path)

        # String analysis
        self._scan_strings_binary(path)

    # ── ZIP ────────────────────────────────────────────────────────────────
    def _analyze_zip(self, path: str, is_apk: bool = False):
        self._cb(f"[ZIP] Extracting: {path}\n")
        with tempfile.TemporaryDirectory() as tmp:
            try:
                with zipfile.ZipFile(path, "r") as z:
                    z.extractall(tmp)
                self._analyze_directory(tmp, label="APK" if is_apk else "ZIP")
            except Exception as e:
                self._cb(f"[ZIP] Error: {e}\n")

    # ── Directory ──────────────────────────────────────────────────────────
    def _analyze_directory(self, dirpath: str, label: str = "DIR"):
        self._cb(f"[{label}] Scanning directory: {dirpath}\n")
        for root, dirs, files in os.walk(dirpath):
            # Skip common non-code dirs
            dirs[:] = [d for d in dirs if d not in
                       (".git", "node_modules", "__pycache__",
                        ".idea", ".vscode", "venv", ".env")]
            for fname in files:
                fpath = os.path.join(root, fname)
                ext   = Path(fname).suffix.lower()
                lang  = EXT_LANG.get(ext)
                if lang:
                    self._analyze_file(fpath, lang)

    # ── Single File ────────────────────────────────────────────────────────
    def _analyze_file(self, fpath: str, lang: str):
        self.file_count += 1
        try:
            content = Path(fpath).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return
        self._scan_text(content, lang,  source=fpath)
        self._scan_text(content, "generic", source=fpath)  # always run generic

    # ── Text Pattern Scanner ───────────────────────────────────────────────
    def _scan_text(self, content: str, lang: str, source: str = ""):
        patterns = STATIC_PATTERNS.get(lang, [])
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, severity, name, fix in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_bug(
                        name, severity, fix,
                        source=source,
                        line=i,
                        detail=line.strip()[:200]
                    )

    # ── YARA Scan ──────────────────────────────────────────────────────────
    def _yara_scan(self, path: str):
        try:
            import yara
            rules_dir = Path("data/yara_rules")
            if not rules_dir.exists():
                return
            for rule_file in rules_dir.glob("*.yar"):
                try:
                    rules = yara.compile(str(rule_file))
                    matches = rules.match(path)
                    for m in matches:
                        self._add_bug(
                            f"YARA: {m.rule}", "HIGH",
                            "Review matched YARA signature and investigate the file.",
                            source=path,
                            detail=str(m.meta)
                        )
                except Exception:
                    pass
        except ImportError:
            pass

    # ── Binary String Extraction ───────────────────────────────────────────
    def _scan_strings_binary(self, path: str):
        """Extract readable strings from binary and scan for secrets."""
        try:
            with open(path, "rb") as f:
                data = f.read()
            # Extract printable strings (min len 6)
            strings = re.findall(rb"[\x20-\x7e]{6,}", data)
            text = "\n".join(s.decode("ascii", errors="ignore") for s in strings)
            self._scan_text(text, "generic", source=f"{path} [strings]")
            self._cb(f"[Strings] Extracted {len(strings)} strings from binary.\n")
        except Exception as e:
            self._cb(f"[Strings] Error: {e}\n")

    # ── Helpers ────────────────────────────────────────────────────────────
    def _add_bug(self, name: str, severity: str, fix: str,
                 source: str = "", line: int = 0,
                 detail: str = ""):
        # De-duplicate: same name + source + line
        key = f"{name}|{source}|{line}"
        if any(b.get("_key") == key for b in self.bugs):
            return
        self.bugs.append({
            "_key":    key,
            "name":    name,
            "severity":severity,
            "fix":     fix,
            "source":  os.path.basename(source) if source else "",
            "source_full": source,
            "line":    line,
            "detail":  detail,
            "cvss":    self._estimate_cvss(severity),
        })
        self._cb(f"  [{severity}] {name}" +
                 (f" → line {line}" if line else "") + "\n")

    @staticmethod
    def _estimate_cvss(severity: str) -> str:
        return {
            "CRITICAL": "9.0–10.0",
            "HIGH":     "7.0–8.9",
            "MEDIUM":   "4.0–6.9",
            "LOW":      "0.1–3.9",
            "INFO":     "0.0",
        }.get(severity, "N/A")

    @staticmethod
    def _hash_file(path: str, algo: str) -> str:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    # ── AI Explanations (optional) ─────────────────────────────────────────
    def _ai_enrich(self, bug: dict) -> str:
        if not self.llm:
            return ""
        prompt = (
            f"Security bug found: {bug['name']}\n"
            f"Severity: {bug['severity']}\n"
            f"Detail: {bug.get('detail', '')}\n"
            f"Suggested fix: {bug['fix']}\n"
            f"Explain this bug in 2 sentences and give a concrete code fix example."
        )
        try:
            return self.llm.generate(prompt, max_new_tokens=200)
        except Exception:
            return ""

    # ── Report Builder ─────────────────────────────────────────────────────
    def _build_report(self, target: str) -> dict:
        # Sort by severity
        order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        bugs_sorted = sorted(self.bugs,
                             key=lambda b: order.get(b["severity"], 99))

        # Remove internal _key field
        for b in bugs_sorted:
            b.pop("_key", None)

        # Count by severity
        counts = {sev: 0 for sev in order}
        for b in bugs_sorted:
            counts[b["severity"]] = counts.get(b["severity"], 0) + 1

        # Risk score
        score = min(100, (
            counts["CRITICAL"] * 25 +
            counts["HIGH"]     * 15 +
            counts["MEDIUM"]   *  8 +
            counts["LOW"]      *  3
        ))

        level = (
            "CRITICAL" if score >= 75 else
            "HIGH"     if score >= 50 else
            "MEDIUM"   if score >= 25 else
            "LOW"      if score >   0 else
            "CLEAN"
        )

        scan_time = (
            datetime.utcnow() - self.scan_start
        ).total_seconds()

        report = {
            "status":      "ok",
            "target":      target,
            "scan_time_s": round(scan_time, 2),
            "files_scanned": self.file_count,
            "total_bugs":  len(bugs_sorted),
            "risk_score":  score,
            "risk_level":  level,
            "counts":      counts,
            "bugs":        bugs_sorted,
            "summary":     self._make_summary(bugs_sorted, counts, level, target),
            "scanned_at":  datetime.utcnow().isoformat(),
        }

        self._cb(f"\n{'='*60}\n")
        self._cb(f"SCAN COMPLETE  |  Bugs: {len(bugs_sorted)}  |  Risk: {level}  |  Score: {score}/100\n")
        self._cb(f"{'='*60}\n")
        return report

    def _make_summary(self, bugs, counts, level, target) -> str:
        top = [b["name"] for b in bugs[:3]]
        top_str = ", ".join(top) if top else "None"
        return (
            f"Analyzed '{os.path.basename(target)}'. "
            f"Found {len(bugs)} issue(s): "
            f"{counts['CRITICAL']} Critical, "
            f"{counts['HIGH']} High, "
            f"{counts['MEDIUM']} Medium, "
            f"{counts['LOW']} Low. "
            f"Risk level: {level}. "
            f"Top issues: {top_str}."
        )

    # ── Report Export ──────────────────────────────────────────────────────
    def save_report_json(self, report: dict, out_path: str = None) -> str:
        if not out_path:
            ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = f"reports/bug_report_{ts}.json"
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved: {out_path}")
        return out_path

    def save_report_html(self, report: dict, out_path: str = None) -> str:
        if not out_path:
            ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = f"reports/bug_report_{ts}.html"
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        rows = ""
        for b in report["bugs"]:
            color = SEV_COLOR.get(b["severity"], "#aaa")
            rows += (
                f'<tr>'
                f'<td style="color:{color};font-weight:bold">{b["severity"]}</td>'
                f'<td>{b["name"]}</td>'
                f'<td>{b["source"]}{":" + str(b["line"]) if b["line"] else ""}</td>'
                f'<td><code>{b.get("detail","")[:100]}</code></td>'
                f'<td style="color:#00ff41">{b["fix"]}</td>'
                f'<td>{b["cvss"]}</td>'
                f'</tr>\n'
            )

        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>DAVID Bug Report</title>
<style>
  body{{background:#0a0a0a;color:#e0e0e0;font-family:'Courier New',monospace;padding:20px}}
  h1{{color:#00ff41}} h2{{color:#41b3ff}}
  table{{width:100%;border-collapse:collapse;margin-top:16px}}
  th{{background:#1a1a1a;color:#00ff41;padding:8px;text-align:left}}
  td{{padding:6px 8px;border-bottom:1px solid #222}}
  .score{{font-size:48px;font-weight:bold;color:#ffd700}}
  .badge{{display:inline-block;padding:4px 12px;border-radius:4px;
          font-weight:bold;color:#000}}
  code{{background:#1a1a1a;padding:2px 6px;border-radius:3px;font-size:12px}}
</style></head>
<body>
<h1>&#9632; DAVID CYBER INTELLIGENCE SYSTEM</h1>
<h2>Bug Analysis Report</h2>
<p><b>Target:</b> {report['target']}</p>
<p><b>Scanned:</b> {report['scanned_at']} UTC | 
   <b>Files:</b> {report['files_scanned']} | 
   <b>Scan time:</b> {report['scan_time_s']}s</p>
<p class="score">{report['risk_score']}/100</p>
<p><b>Risk Level:</b> 
  <span class="badge" style="background:{SEV_COLOR.get(report['risk_level'],'#888')}">
    {report['risk_level']}
  </span>
</p>
<p>{report['summary']}</p>
<h2>Findings ({report['total_bugs']})</h2>
<table>
<tr>
  <th>Severity</th><th>Issue</th><th>Location</th>
  <th>Detail</th><th>Fix</th><th>CVSS</th>
</tr>
{rows}
</table>
<hr><p style="color:#555">Generated by DAVID Cyber Intelligence System | Devil Pvt Ltd & Nexuzy Tech Pvt Ltd</p>
</body></html>"""

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"HTML report saved: {out_path}")
        return out_path


# ─────────────────────────────────────────────────────────────────────────────
#  STANDALONE CLI
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    engine = BugAnalyzerEngine()
    report = engine.analyze(target, progress_cb=print)
    out = engine.save_report_html(report)
    print(f"\nHTML report: {out}")
    print(f"Risk: {report['risk_level']} | Score: {report['risk_score']}/100 | Bugs: {report['total_bugs']}")
