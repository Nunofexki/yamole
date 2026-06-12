from fpdf import FPDF

class WriteupPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "CTF Writeup - Fiat 600 (Medium Crypto)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def title_page(self):
        self.add_page()
        self.ln(50)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(30, 30, 30)
        self.cell(0, 15, "Fiat 600", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 16)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, "Medium Cryptography Challenge - Writeup", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        self.set_draw_color(50, 100, 200)
        self.set_line_width(0.5)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, '"What about fiat seicento? We bet you can drive this one as well."', align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, "Category: Cryptography", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "Difficulty: Medium", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "Type: Interactive (netcat)", align="C", new_x="LMARGIN", new_y="NEXT")

    def section(self, title):
        self.ln(6)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(50, 100, 200)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(50, 100, 200)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def subsection(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6.5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        y = self.get_y()
        lines = code.split("\n")
        h = len(lines) * 5 + 6
        if y + h > 270:
            self.add_page()
            y = self.get_y()
        self.set_draw_color(200, 200, 200)
        self.rect(10, y, 190, h)
        self.set_xy(12, y + 3)
        for line in lines:
            self.cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
            self.set_x(12)
        self.ln(4)
        self.set_font("Helvetica", "", 11)


pdf = WriteupPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# Title Page
pdf.title_page()

# Background
pdf.add_page()
pdf.section("1. Background: Schnorr Identification Protocol")

pdf.body(
    "The Schnorr identification protocol is a zero-knowledge proof system that allows "
    "someone (the Prover) to convince someone else (the Verifier) that they know a secret "
    "key, without revealing the secret itself.\n\n"
    "It works in a group of prime order Q with a generator g. The Prover has:\n"
    "  - Private key: x (a random secret number)\n"
    "  - Public key: H = g^x mod Q\n\n"
    "The protocol has three steps:"
)

pdf.subsection("1.1 The Three Steps")
pdf.body(
    "Step 1 - COMMITMENT: The Prover picks a random number r and computes:\n"
    "    u = g^r mod Q\n"
    "  The Prover sends u to the Verifier.\n\n"
    "Step 2 - CHALLENGE: The Verifier sends a random challenge c to the Prover.\n"
    "  (In non-interactive mode, c = Hash(g, Q, H, u))\n\n"
    "Step 3 - RESPONSE: The Prover computes:\n"
    "    z = r + x * c  (mod Q)\n"
    "  The Prover sends z to the Verifier.\n\n"
    "The Verifier checks that: g^z == u * H^c mod Q\n\n"
    "This works because: g^z = g^(r+xc) = g^r * g^(xc) = u * (g^x)^c = u * H^c"
)

pdf.subsection("1.2 Why Is It Secure?")
pdf.body(
    "The security relies on the fact that the challenge c MUST depend on the commitment u. "
    "If c is computed BEFORE u is known, or if c does not include u in its computation, "
    "then the Prover can cheat! This is the critical point exploited in this challenge."
)

# Challenge Analysis
pdf.add_page()
pdf.section("2. Challenge Analysis")

pdf.subsection("2.1 The Server Code")
pdf.body("The server implements a Schnorr verification scheme. The key function is SchnorrVerify:")
pdf.code_block(
    "def SchnorrVerify(h, u, c, z):\n"
    "    if u * h * z % Q == 0:\n"
    "        return False\n"
    "\n"
    "    tuple_hash = TupleHash128.new(digest_bytes=400)\n"
    "    tuple_hash.update(GENERATOR.to_bytes(400, 'big'))\n"
    "    tuple_hash.update(Q.to_bytes(400, 'big'))\n"
    "    tuple_hash.update(h.to_bytes(400, 'big'))\n"
    "\n"
    "    c_prime = int.from_bytes(tuple_hash.digest(), 'big')\n"
    "\n"
    "    hashes_match = c == c_prime\n"
    "    valid_eq = pow(GENERATOR, z, Q) == u * pow(h, c, Q) % Q\n"
    "\n"
    "    return hashes_match and valid_eq"
)

pdf.subsection("2.2 The Vulnerability")
pdf.body(
    "Look carefully at what goes INTO the hash:\n\n"
    "    c = Hash(GENERATOR, Q, h)\n\n"
    "In a CORRECT Schnorr protocol, the hash should be:\n\n"
    "    c = Hash(GENERATOR, Q, h, u)    <-- 'u' is MISSING!\n\n"
    "The commitment 'u' is NOT included in the hash! This means the challenge 'c' is a "
    "FIXED, DETERMINISTIC value that depends only on the public parameters (g, Q) and the "
    "public key (H). Anyone can compute it without knowing the private key.\n\n"
    "This completely breaks the security of the protocol."
)

pdf.subsection("2.3 Why Missing 'u' Breaks Everything")
pdf.body(
    "In the correct protocol, the Prover must:\n"
    "  1. First commit to u = g^r (choose r randomly)\n"
    "  2. Then receive/compute c = Hash(..., u)\n"
    "  3. Then compute z = r + x*c\n\n"
    "The Prover needs to know x (the private key) to compute z in step 3, because r was "
    "already fixed in step 1 before c was known.\n\n"
    "But if c doesn't depend on u, an attacker can:\n"
    "  1. First compute c (since it's deterministic)\n"
    "  2. Choose any z (e.g., z = 1337)\n"
    "  3. COMPUTE u backwards: u = g^z * H^(-c) mod Q\n\n"
    "This satisfies the verification equation g^z == u * H^c because:\n"
    "  u * H^c = g^z * H^(-c) * H^c = g^z  (checkmark!)\n\n"
    "No private key needed!"
)

# The Attack
pdf.add_page()
pdf.section("3. The Attack")

pdf.subsection("3.1 Step-by-Step Forgery")
pdf.body(
    "Given only the public key H (printed by the server), we forge a valid proof:\n\n"
    "1. Compute the deterministic challenge:\n"
    "   c = TupleHash128(GENERATOR || Q || H)\n\n"
    "2. Pick any z (we choose z = 1337, any non-zero value works):\n"
    "   z = 1337\n\n"
    "3. Compute u by rearranging the verification equation:\n"
    "   g^z == u * H^c mod Q\n"
    "   u = g^z * H^(-c) mod Q\n"
    "   u = pow(2, 1337, Q) * pow(H, -c, Q) % Q\n\n"
    "4. Submit (u, c, z) to the server. It verifies and gives us the flag!"
)

pdf.subsection("3.2 Complete Exploit Code")
pdf.code_block(
    "from pwn import *\n"
    "from Crypto.Hash import TupleHash128\n"
    "\n"
    "GENERATOR = 0x2\n"
    "Q = 4863582...  # (large prime, from source)\n"
    "\n"
    "r = remote('challenges.cybersecuritychallenge.pt', 24303)\n"
    "r.recvuntil(b'public key: ')\n"
    "H = int(r.recvline().strip())\n"
    "\n"
    "# Compute deterministic c (the bug: no 'u' in hash!)\n"
    "tuple_hash = TupleHash128.new(digest_bytes=400)\n"
    "tuple_hash.update(GENERATOR.to_bytes(400, 'big'))\n"
    "tuple_hash.update(Q.to_bytes(400, 'big'))\n"
    "tuple_hash.update(H.to_bytes(400, 'big'))\n"
    "c = int.from_bytes(tuple_hash.digest(), 'big')\n"
    "\n"
    "# Forge: choose z, compute u backwards\n"
    "z = 1337\n"
    "u = (pow(GENERATOR, z, Q) * pow(H, -c, Q)) % Q\n"
    "\n"
    "# Submit forged proof\n"
    "r.sendlineafter(b'choice: ', b'1')\n"
    "r.sendlineafter(b'u: ', str(u).encode())\n"
    "r.sendlineafter(b'c: ', str(c).encode())\n"
    "r.sendlineafter(b'z: ', str(z).encode())\n"
    "print(r.recvall(timeout=5).decode())"
)

# Verification
pdf.add_page()
pdf.section("4. Local Verification")
pdf.body(
    "Since the CTF server may not always be available, we can verify the exploit locally "
    "by simulating the server. The script below proves the forgery works against ANY "
    "randomly generated private key:"
)
pdf.code_block(
    "from Crypto.Util.number import getRandomInteger\n"
    "from Crypto.Hash import TupleHash128\n"
    "\n"
    "# Server generates a key pair (we DON'T know x)\n"
    "x = getRandomInteger(3071)\n"
    "H = pow(GENERATOR, x, Q)\n"
    "\n"
    "# Attacker computes c (deterministic, no u!)\n"
    "th = TupleHash128.new(digest_bytes=400)\n"
    "th.update(GENERATOR.to_bytes(400, 'big'))\n"
    "th.update(Q.to_bytes(400, 'big'))\n"
    "th.update(H.to_bytes(400, 'big'))\n"
    "c = int.from_bytes(th.digest(), 'big')\n"
    "\n"
    "# Forge proof\n"
    "z = 1337\n"
    "u = (pow(GENERATOR, z, Q) * pow(H, -c, Q)) % Q\n"
    "\n"
    "# Verify: this PASSES!\n"
    "assert SchnorrVerify(H, u, c, z) == True\n"
    "print('Forgery successful!')"
)

pdf.body("Output: Forgery successful! (Tested and confirmed.)")

# Correct vs Broken
pdf.section("5. Correct vs. Broken Protocol")
pdf.subsection("5.1 Side-by-Side Comparison")
pdf.body(
    "BROKEN (this challenge):\n"
    "  c = Hash(g, Q, H)          <-- u NOT included\n"
    "  Result: c is predictable, proof is forgeable\n\n"
    "CORRECT Schnorr:\n"
    "  c = Hash(g, Q, H, u)       <-- u IS included\n"
    "  Result: c depends on the commitment, unforgeable\n\n"
    "When u is included in the hash, the attacker faces a chicken-and-egg problem:\n"
    "  - To compute u backwards, you need to know c first\n"
    "  - But c depends on u (via the hash)\n"
    "  - Finding u such that Hash(..., u) yields a c that satisfies the equation\n"
    "    is computationally infeasible (requires breaking the hash function)"
)

# Lessons
pdf.add_page()
pdf.section("6. Lessons Learned")

pdf.subsection("6.1 The Fiat-Shamir Heuristic Must Include the Commitment")
pdf.body(
    "The Fiat-Shamir heuristic converts an interactive proof into a non-interactive one "
    "by replacing the verifier's random challenge with a hash. The hash MUST include ALL "
    "messages sent before the challenge, especially the commitment (u). Omitting it "
    "makes the proof trivially forgeable.\n\n"
    "The challenge name 'Fiat 600' is a pun on the Fiat-Shamir transform and the "
    "Fiat car brand."
)

pdf.subsection("6.2 Understanding the Math")
pdf.body(
    "The verification equation is:  g^z = u * H^c  (mod Q)\n\n"
    "If the attacker can choose u AFTER knowing c, they can solve for u:\n"
    "  u = g^z / H^c = g^z * H^(-c)  (mod Q)\n\n"
    "This is trivial modular arithmetic. The ONLY thing that prevents this in a "
    "correct protocol is that c must depend on u, creating a circular dependency "
    "that cannot be broken without knowing the discrete log (private key x)."
)

pdf.section("7. Summary")
pdf.body(
    "This challenge implemented a flawed Schnorr identification scheme where the "
    "non-interactive challenge hash omitted the commitment value 'u'. This allowed "
    "us to:\n\n"
    "  1. Compute the deterministic challenge c from public information\n"
    "  2. Choose an arbitrary response z\n"
    "  3. Compute the commitment u backwards to satisfy the verification equation\n"
    "  4. Submit the forged proof (u, c, z) to get the flag\n\n"
    "The fix is simple: include u in the hash computation.\n\n"
    "Flag: CSCPT{...} (obtained from remote server)"
)

# Save
out_path = "/Users/ctw03464/Documents/CTF/yamole/challs/crypto/medium/fiat600/writeup.pdf"
pdf.output(out_path)
print(f"PDF written to {out_path}")
