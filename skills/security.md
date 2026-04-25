# Security Audit Skill

> **name**: security
> **description**: Full-stack security auditor for web applications. Use this skill whenever the user wants to analyze, audit, harden, or scan their website or web app for vulnerabilities. Triggers include: "check my site for vulnerabilities", "security audit", "find security issues", "harden my app", "scan for XSS / SQL injection / CSRF", "check my headers", "pentest my site", "is my site secure", "check my dependencies for CVEs", or any mention of OWASP, security misconfigurations, exposed secrets, or authentication weaknesses. Always use this skill when security is the primary concern.

---

## How to Use This Skill

1. **Gather context** — ask the user for their stack, URL (if live), and codebase access
2. **Run the audit pipeline** — execute each phase in order (or in parallel where possible)
3. **Score and prioritize findings** — use CVSS-style severity (Critical / High / Medium / Low / Info)
4. **Deliver the report** — structured markdown with remediation steps per finding
5. **Offer a remediation pass** — optionally fix issues directly in the code

---

## Phase 1 — Reconnaissance & Asset Mapping

Before testing, map the full attack surface.

### Tools to use

```bash
# DNS enumeration
dig +short <domain> ANY
nslookup -type=ANY <domain>
host -a <domain>

# Subdomain discovery
subfinder -d <domain> -silent
amass enum -passive -d <domain>

# Fallback: check crt.sh for certificate transparency logs
curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq '.[].name_value' | sort -u

# Port scanning
nmap -sV -sC -p- --min-rate 5000 <ip_or_domain>
nmap -sU -top-ports 200 <ip_or_domain>  # UDP scan

# Technology fingerprinting
whatweb <url>
curl -sI <url>  # grab raw headers
```

### What to look for

- Exposed subdomains (admin., api., staging., dev., test., beta.)
- Open ports beyond 80/443 (databases, Redis, Elasticsearch exposed publicly)
- Server version disclosure in headers (Apache/2.4.1, PHP/7.2.x)
- Technology stack fingerprint → map known CVEs per version
- DNS misconfigurations (dangling CNAME, zone transfer enabled)

```bash
# Test for DNS zone transfer vulnerability
dig axfr <domain> @<nameserver>
```

---

## Phase 2 — HTTP Security Headers Audit

Missing or misconfigured headers are a top source of vulnerabilities.

### Run the check

```bash
curl -sI https://<domain> | grep -Ei \
  "strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy|cross-origin|cache-control"
```

### Headers checklist

| Header | Required Value | Risk if missing |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | SSL stripping, MitM |
| `Content-Security-Policy` | Restrictive policy | XSS, data injection |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Clickjacking |
| `X-Content-Type-Options` | `nosniff` | MIME-type sniffing |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Data leakage |
| `Permissions-Policy` | Restrict camera/mic/geo | Feature abuse |
| `Cross-Origin-Opener-Policy` | `same-origin` | XS-Leaks |
| `Cross-Origin-Embedder-Policy` | `require-corp` | Spectre attacks |
| `Cross-Origin-Resource-Policy` | `same-origin` or `same-site` | Data leakage |
| `Cache-Control` | `no-store` on sensitive pages | Credential caching |

### Flag

- Missing CSP → **High**
- Missing HSTS → **High**
- Missing X-Frame-Options → **Medium**
- Server version in headers → **Medium**
- `X-Powered-By` header exposed → **Low**

---

## Phase 3 — TLS / SSL Configuration

```bash
# Full TLS scan
testssl.sh --full <domain>

# Quick check with nmap
nmap --script ssl-enum-ciphers -p 443 <domain>

# Certificate check
openssl s_client -connect <domain>:443 -showcerts </dev/null 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer
```

### What to flag

- TLS 1.0 or 1.1 enabled → **High** (POODLE, BEAST)
- SSLv3 enabled → **Critical**
- Weak ciphers (RC4, 3DES, NULL, EXPORT) → **High**
- Certificate expired or self-signed in production → **Critical**
- Certificate not covering all subdomains → **Medium**
- HSTS not preloaded → **Low**
- Missing OCSP stapling → **Info**

---

## Phase 4 — Injection Vulnerabilities

### SQL Injection

```bash
# Automated scan with sqlmap
sqlmap -u "https://<domain>/page?id=1" --batch --level=3 --risk=2 \
  --dbs --random-agent

# With POST data
sqlmap -u "https://<domain>/login" --data="user=admin&pass=test" \
  --batch --level=3
```

**Manual payloads to test in every input field:**
```
'
''
`
')
'))
' OR '1'='1
' OR '1'='1'--
' OR 1=1--
1' ORDER BY 1--
1' UNION SELECT null--
```

### XSS (Cross-Site Scripting)

```bash
# Automated
dalfox url "https://<domain>/search?q=test" --silence
```

**Manual payloads:**
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
"><script>alert(document.cookie)</script>
javascript:alert(1)
<svg onload=alert(1)>
{{7*7}}        <!-- template injection probe -->
${7*7}         <!-- EL injection -->
```

Check: URL params, form fields, HTTP headers (User-Agent, Referer), JSON body fields, file upload names.

### Command Injection

```bash
; id
| id
`id`
$(id)
& id
&& id
; sleep 5
| sleep 5
```

### Path Traversal / LFI

```
../../etc/passwd
....//....//etc/passwd
%2e%2e%2fetc%2fpasswd
..%252f..%252fetc/passwd
/proc/self/environ
```

### SSRF (Server-Side Request Forgery)

```
http://127.0.0.1/admin
http://169.254.169.254/latest/meta-data/   # AWS metadata
http://metadata.google.internal/            # GCP metadata
file:///etc/passwd
```

---

## Phase 5 — Authentication & Session Security

### Checklist

- **No rate limiting on login** → brute-force possible → **High**
- **Username enumeration** via different error messages → **Medium**
- **Weak session tokens** (short, sequential, guessable) → **High**
- **Session not invalidated on logout** → **High**
- **JWT with `alg: none`** → **Critical**
- **No MFA on admin accounts** → **High**
- **Password reset tokens not expiring** → **Medium**
- **Insecure "remember me" cookie** → **Medium**

### CSRF Check

```bash
# Look for CSRF token in forms
curl -s <url> | grep -i "csrf\|_token\|authenticity_token"

# Check if state-changing requests can be made without token
curl -X POST <action_url> \
  -H "Origin: https://evil.com" \
  -H "Referer: https://evil.com" \
  -d "action=delete&id=1"
```

---

## Phase 6 — Dependency & CVE Scanning

### JavaScript / Node.js

```bash
npm audit --json
npx snyk test
```

### Python

```bash
pip-audit --json
safety check --full-report
bandit -r . -f json
```

### Docker images

```bash
trivy image <image_name>
grype <image_name>
```

### General

```bash
# OSV Scanner (multi-language)
osv-scanner --recursive .
```

**Flag all Critical and High CVEs immediately. Include CVE ID, CVSS score, affected version, and patched version.**

---

## Phase 7 — Source Code Static Analysis (SAST)

```bash
# Universal — Semgrep
semgrep --config=auto .
semgrep --config "p/owasp-top-ten" .
semgrep --config "p/secrets" .
```

### Patterns to look for manually

```bash
# Hardcoded secrets
grep -rn "password\s*=\s*['\"]" . --include="*.js" --include="*.py" --include="*.php"
grep -rn "api_key\s*=\s*['\"]" .
grep -rn "AWS_SECRET\|PRIVATE_KEY\|BEGIN RSA" .

# Dangerous functions
grep -rn "eval(" .
grep -rn "innerHTML\s*=" .  # XSS risk
grep -rn "dangerouslySetInnerHTML" .  # React XSS

# SQL injection risks
grep -rn "query.*\$_GET\|query.*\$_POST\|\\.format.*sql\|f\".*SELECT" .
```

---

## Phase 8 — Secrets & Credentials Scanning

```bash
# Trufflehog
trufflehog git file://. --json

# Gitleaks
gitleaks detect --source . --verbose

# Grep patterns
grep -rn "-----BEGIN" .           # Private keys
grep -rn "ghp_\|ghs_\|gho_" .   # GitHub tokens
grep -rn "sk-[a-zA-Z0-9]{48}" . # OpenAI keys
grep -rn "AKIA[0-9A-Z]{16}" .   # AWS access keys
grep -rn "eyJ" .                  # JWTs in code
```

### Check exposed files

```bash
for f in .env .env.local .env.production config.php wp-config.php \
          database.yml secrets.yml id_rsa .htpasswd web.config \
          phpinfo.php server-status backup.sql dump.sql; do
  curl -so /dev/null -w "%{http_code} $f\n" https://<domain>/$f
done
```

---

## Phase 9 — Infrastructure & Configuration

### Server Misconfigurations

```bash
# Directory listing
curl -s https://<domain>/images/ | grep -i "index of"

# Common admin panels exposed
for path in admin wp-admin phpmyadmin adminer.php \
            manager/html jenkins grafana kibana; do
  curl -so /dev/null -w "%{http_code} /$path\n" https://<domain>/$path
done

# Exposed development files
for f in .git/HEAD .svn/entries .DS_Store Dockerfile \
          docker-compose.yml package.json composer.json \
          Makefile .travis.yml .github/workflows/; do
  curl -so /dev/null -w "%{http_code} $f\n" https://<domain>/$f
done
```

### .git Exposure Check

```bash
curl -s https://<domain>/.git/HEAD
# If returns "ref: refs/heads/main" → CRITICAL
```

---

## Phase 10 — API Security Audit

```bash
# Discover API endpoints
ffuf -u https://<domain>/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,204,301,302,307,401,403

# Check for exposed API documentation
for path in api/docs swagger swagger-ui openapi.json api-docs graphql; do
  curl -so /dev/null -w "%{http_code} /$path\n" https://<domain>/$path
done
```

### API-specific checks

- **BOLA / IDOR**: Change IDs in requests (`/api/users/123` → `/api/users/124`)
- **Mass assignment**: Send extra fields in POST/PUT body
- **Verbose errors**: Stack traces / SQL errors in API responses
- **Rate limiting**: Flood endpoints without auth

---

## Phase 11 — OWASP Top 10 Compliance Checklist

| # | Category | Key Tests |
|---|---|---|
| A01 | Broken Access Control | IDOR, privilege escalation, CORS misconfiguration |
| A02 | Cryptographic Failures | Weak TLS, unencrypted PII, hardcoded secrets |
| A03 | Injection | SQLi, XSS, Command injection, SSTI |
| A04 | Insecure Design | Missing rate limits, no abuse prevention |
| A05 | Security Misconfiguration | Headers, default credentials, debug mode on |
| A06 | Vulnerable Components | CVEs in deps, outdated frameworks |
| A07 | Auth Failures | Weak passwords, no MFA, session issues |
| A08 | Software Integrity Failures | No SRI on CDN scripts, unsigned artifacts |
| A09 | Logging Failures | No audit logs, sensitive data in logs |
| A10 | SSRF | URL parameters hitting internal services |

---

## Severity Scoring

| Severity | CVSS | Action |
|---|---|---|
| **Critical** | 9.0-10.0 | Fix immediately, notify stakeholders |
| **High** | 7.0-8.9 | Fix within 24-48h |
| **Medium** | 4.0-6.9 | Fix within 1 sprint |
| **Low** | 1.0-3.9 | Fix in next release |
| **Info** | 0.0 | Best practice improvement |

---

## Output Report Format

For every finding:

```
### [SEVERITY] Finding Title
**Category**: OWASP A0X / CWE-XXX
**Affected**: URL, file, or component
**CVSS Score**: X.X
**Description**: What the vulnerability is and why it's dangerous.
**Evidence**: Request/response proof or curl command
**Impact**: What an attacker could do if exploited.
**Remediation**:
  1. Step-by-step fix
  2. Code example if applicable
  3. Reference: https://...
```

---

## Remediation Pass (Optional)

After the audit, offer to:

1. **Fix headers** — add security headers to config
2. **Patch dependencies** — run `npm audit fix` or update requirements
3. **Remove secrets** — replace hardcoded secrets with env vars
4. **Harden auth** — implement rate limiting, add CSRF protection, secure cookies
5. **Update CSP** — generate a strict Content-Security-Policy

---

## Quick Start (One-liner audit)

```bash
# 1. Headers
curl -sI https://<domain>
# 2. SSL
testssl.sh --quiet https://<domain>
# 3. Common misconfigs
nuclei -u https://<domain> -t misconfigurations/ -t exposures/ -silent
# 4. Deps (in project folder)
npm audit && semgrep --config=auto . && gitleaks detect --source .
```

---

*Always get written authorization before testing any system you do not own. Security testing without permission is illegal.*
