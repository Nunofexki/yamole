from fpdf import FPDF

class WriteupPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "CTF Writeup - XOR-Prime (Hard Crypto)", align="C", new_x="LMARGIN", new_y="NEXT")
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
        self.cell(0, 15, "XOR-Prime", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 16)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, "Hard Cryptography Challenge - Writeup", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        self.set_draw_color(200, 50, 50)
        self.set_line_width(0.5)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, '"They asked me to generate two RSA keys in a low entropy environment.\nI came up with something that only needs half of the usual entropy!\nI doubt it will be possible but try to break it anyway..."', align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, "Category: Cryptography", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "Difficulty: Hard", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "Flag: CSCPT{d0nt_us3_rel4ted_pr1mes}", align="C", new_x="LMARGIN", new_y="NEXT")

    def section(self, title):
        self.ln(6)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(180, 40, 40)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(180, 40, 40)
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
        x = self.get_x()
        y = self.get_y()
        # Calculate height needed
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

    def bullet(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(8, 6.5, "-")
        self.multi_cell(0, 6.5, text)

    def bold_inline(self, label, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(self.get_string_width(label) + 2, 6.5, label)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6.5, text)

pdf = WriteupPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ─── Title Page ───
pdf.title_page()

# ─── Page 2: Background ───
pdf.add_page()
pdf.section("1. Background: What is RSA?")

pdf.body(
    "RSA is one of the most widely used public-key cryptosystems. It relies on the mathematical "
    "difficulty of factoring the product of two large prime numbers. Here is a simplified overview:"
)

pdf.subsection("1.1 Key Generation")
pdf.body(
    "1. Choose two large, random, distinct prime numbers p and q (typically 512 bits each).\n"
    "2. Compute N = p * q. This is the public modulus (1024 bits).\n"
    "3. Compute the totient: phi(N) = (p - 1) * (q - 1).\n"
    "4. Choose a public exponent e (commonly 65537).\n"
    "5. Compute the private exponent d such that e * d = 1 (mod phi(N)).\n"
    "6. Public key: (N, e). Private key: d."
)

pdf.subsection("1.2 Encryption and Decryption")
pdf.body(
    "To encrypt a message m:  c = m^e mod N\n"
    "To decrypt a ciphertext c:  m = c^d mod N\n\n"
    "The security of RSA depends entirely on the fact that an attacker who only knows N "
    "cannot efficiently find p and q. If p and q are found, the attacker can compute d "
    "and decrypt any message."
)

pdf.subsection("1.3 Why Primes Must Be Independent")
pdf.body(
    "A critical requirement of RSA is that each key pair uses independently generated primes. "
    "If multiple RSA keys share factors, or if the primes are mathematically related, an attacker "
    "can exploit these relationships to recover the factors. This challenge demonstrates exactly "
    "such a flaw."
)

# ─── Page: Challenge Analysis ───
pdf.add_page()
pdf.section("2. Challenge Analysis")

pdf.subsection("2.1 The Source Code")
pdf.body("We are given the following Python script (gen_keys.py):")
pdf.code_block(
    "from Crypto.Util.number import *\n"
    "from pwn import xor\n"
    "from flag import FLAG\n"
    "\n"
    "p1 = getPrime(512)\n"
    "q1 = getPrime(512)\n"
    "BITS = 2**512\n"
    "\n"
    "def generate_prime(p, q, start):\n"
    "    i = start\n"
    "    while 1:\n"
    "        i += 1\n"
    "        r = (pow(p, i, BITS) ^ pow(q, i, BITS)) + 1\n"
    "        if isPrime(r):\n"
    "            return r, i\n"
    "\n"
    "p2, k = generate_prime(p1, q1, 0)\n"
    "q2, l = generate_prime(p1, q1, k+1)\n"
    "\n"
    "N1 = p1*q1\n"
    "N2 = p2*q2\n"
    "e = 65537\n"
    "\n"
    "print('N1 =', N1)\n"
    "print('N2 =', N2)\n"
    "print('c =', pow(FLAG, e, N1))\n"
    "print('And its fast too, only took', l, 'iterations')"
)

pdf.subsection("2.2 The Output")
pdf.body("And we are given the output (output.txt) with the following values:")
pdf.code_block(
    "N1 = 7713706983181812380724077445595076276799...(truncated)\n"
    "N2 = 5525732987607991393746708411247537346817...(truncated)\n"
    "c  = 5895927874393764585159138201376040175359...(truncated)\n"
    "And its fast too, only took 228 iterations in total"
)

pdf.subsection("2.3 Understanding the Vulnerability")
pdf.body(
    "The challenge description says: \"only needs half of the usual entropy.\" This is the key hint. "
    "Normally, two RSA keys require four independently random primes (p1, q1, p2, q2). But here, "
    "only p1 and q1 are randomly generated. The primes p2 and q2 are deterministically derived "
    "from p1 and q1 using the formula:"
)
pdf.code_block("r = (pow(p1, i, 2^512) ^ pow(q1, i, 2^512)) + 1")
pdf.body(
    "This means p2 and q2 are completely determined by p1 and q1. There is a mathematical "
    "relationship between the two RSA moduli N1 and N2. We can exploit this relationship "
    "to recover p1 and q1, and then decrypt the flag."
)

# ─── Page: The XOR Property ───
pdf.add_page()
pdf.section("3. The Key Insight: XOR is Bitwise")

pdf.body(
    "The XOR (exclusive or) operation works bit by bit. This means that bit j of the result "
    "(p1^i XOR q1^i) only depends on bits 0 through j of the inputs. Similarly, "
    "modular exponentiation mod 2^b only depends on the lowest b bits of the base."
)

pdf.subsection("3.1 What Does This Mean?")
pdf.body(
    "If we know the lowest b bits of p1, we can:\n\n"
    "  1. Compute the lowest b bits of q1, because p1 * q1 = N1, so:\n"
    "     q1 mod 2^b = N1 * (p1)^(-1) mod 2^b\n\n"
    "  2. Compute the lowest b bits of p2 and q2, because:\n"
    "     p2 mod 2^b = (p1^k mod 2^b  XOR  q1^k mod 2^b) + 1  mod 2^b\n"
    "     q2 mod 2^b = (p1^228 mod 2^b  XOR  q1^228 mod 2^b) + 1  mod 2^b\n\n"
    "  3. Check if p2 * q2 = N2 mod 2^b\n\n"
    "This lets us build up p1 one bit at a time, from the least significant bit to the most "
    "significant bit. At each step, we try both possibilities (0 or 1 for the next bit) and "
    "keep only the ones that satisfy ALL constraints."
)

pdf.subsection("3.2 This Technique Is Called \"2-adic Lifting\"")
pdf.body(
    "This technique is related to Hensel's Lemma, a classical result in number theory. "
    "It works whenever equations involve operations that are \"local\" in the 2-adic sense "
    "-- meaning that the low bits of the output depend only on the low bits of the input. "
    "Both multiplication mod 2^b and XOR have this property, which is why the attack works."
)

# ─── Page: Attack Step by Step ───
pdf.add_page()
pdf.section("4. The Attack, Step by Step")

pdf.subsection("Step 1: Determine the Iteration Indices k and l")
pdf.body(
    "From the output, we know l = 228 (total iterations). This means q2 was generated at "
    "iteration i = 228. We do NOT know k (the iteration for p2). However, k must be between "
    "1 and 226 (since q2 starts searching at k+2 and finishes at 228).\n\n"
    "Our strategy: try each possible k value (1 to 226) and see which one allows the "
    "bit-by-bit recovery to succeed (i.e., candidates survive all 512 bit levels)."
)

pdf.subsection("Step 2: Initialize the Bit-by-Bit Search")
pdf.body(
    "We know that p1 is an odd prime, so its least significant bit is 1. We start with:\n"
    "  candidates = {1}   (p1 mod 2 = 1)\n\n"
    "Then for each bit position b from 2 to 512:"
)

pdf.subsection("Step 3: Extend Each Candidate")
pdf.body(
    "For each candidate p1_low (which represents p1 mod 2^(b-1)), we try two extensions:\n"
    "  - p1_try = p1_low  (new bit = 0)\n"
    "  - p1_try = p1_low + 2^(b-1)  (new bit = 1)\n\n"
    "For each p1_try, we compute q1_try = N1 * p1_try^(-1) mod 2^b."
)

pdf.subsection("Step 4: Apply the N2 Constraint")
pdf.body(
    "We compute:\n"
    "  p2_mod = (p1_try^k  XOR  q1_try^k) + 1  mod 2^b\n"
    "  q2_mod = (p1_try^228  XOR  q1_try^228) + 1  mod 2^b\n\n"
    "Then check if p2_mod * q2_mod = N2 mod 2^b. If yes, keep this candidate. If no, discard it.\n\n"
    "This constraint eliminates roughly half the candidates at each bit level, preventing "
    "exponential blowup."
)

pdf.subsection("Step 5: Final Verification")
pdf.body(
    "After processing all 512 bits, we have a set of candidates for p1 mod 2^512. Since p1 is "
    "a 512-bit prime, p1 mod 2^512 = p1 itself. We check which candidates actually divide N1. "
    "The one that does is the real p1."
)

# ─── Page: Solution Code ───
pdf.add_page()
pdf.section("5. Complete Solution Code")

pdf.body("Below is the complete, working exploit script (solve_final.py):")

pdf.code_block(
    "from Crypto.Util.number import long_to_bytes\n"
    "\n"
    "N1 = 77137069831818123807240774455950762767990413325793\n"
    "     ...  # (full value in solve_final.py)\n"
    "N2 = 55257329876079913937467084112475373468177837748963\n"
    "     ...  # (full value in solve_final.py)\n"
    "c  = 58959278743937645851591382013760401753597451260953\n"
    "     ...  # (full value in solve_final.py)\n"
    "e = 65537\n"
    "BITS_MOD = 2**512\n"
    "k_val = 210   # found by scanning\n"
    "l_val = 228   # given in the output"
)
pdf.ln(2)
pdf.code_block(
    "candidates = {1}   # p1 is odd\n"
    "for b in range(2, 513):\n"
    "    mod = 1 << b\n"
    "    n1_mod = N1 % mod\n"
    "    n2_mod = N2 % mod\n"
    "    new_candidates = set()\n"
    "    for p1_low in candidates:\n"
    "        for bit in [0, 1]:\n"
    "            p1_try = p1_low | (bit << (b - 1))\n"
    "            q1_try = (n1_mod * pow(p1_try,-1,mod)) % mod\n"
    "            p2 = ((pow(p1_try,k_val,mod) ^\n"
    "                   pow(q1_try,k_val,mod)) + 1) % mod\n"
    "            q2 = ((pow(p1_try,l_val,mod) ^\n"
    "                   pow(q1_try,l_val,mod)) + 1) % mod\n"
    "            if (p2 * q2) % mod == n2_mod:\n"
    "                new_candidates.add(p1_try)\n"
    "    candidates = new_candidates"
)
pdf.ln(2)
pdf.code_block(
    "for p1 in candidates:\n"
    "    if N1 % p1 == 0:\n"
    "        q1 = N1 // p1\n"
    "        phi = (p1 - 1) * (q1 - 1)\n"
    "        d = pow(e, -1, phi)\n"
    "        flag = long_to_bytes(pow(c, d, N1))\n"
    "        print(flag)\n"
    "        # b'CSCPT{d0nt_us3_rel4ted_pr1mes}'"
)

pdf.subsection("5.1 Finding k = 210")
pdf.body(
    "To find k, we run the bit-by-bit search for each candidate k from 1 to 226. For wrong "
    "values of k, the constraint p2*q2 = N2 mod 2^b will become inconsistent early on, and "
    "all candidates will be eliminated. For k = 210, candidates survive all 512 levels, "
    "confirming it is the correct value. This scanning step takes a few minutes but is fully "
    "automated."
)

# ─── Page: Lessons ───
pdf.add_page()
pdf.section("6. Why This Matters: Lessons Learned")

pdf.subsection("6.1 Never Reuse Entropy Across Keys")
pdf.body(
    "The fundamental flaw is that two RSA keys were generated using the same source of "
    "randomness (p1 and q1). The primes p2 and q2 are entirely determined by p1 and q1. "
    "This creates a mathematical link between N1 and N2 that should never exist.\n\n"
    "In real-world cryptography, every prime must be generated from an independent, "
    "high-quality entropy source. Standards like NIST SP 800-90A specify how to properly "
    "seed random number generators for key generation."
)

pdf.subsection("6.2 XOR Does Not Provide Cryptographic Independence")
pdf.body(
    "The author tried to create \"new\" primes by XOR-ing powers of existing primes. While "
    "XOR is used extensively in cryptography (e.g., in stream ciphers and block ciphers), "
    "it does not magically create independent values. The bit-by-bit structure of XOR is "
    "precisely what allows the 2-adic lifting attack."
)

pdf.subsection("6.3 Modular Arithmetic mod 2^n is Weak")
pdf.body(
    "Working modulo 2^512 (a power of 2) is inherently weaker than working modulo a prime. "
    "Powers of 2 have a very special algebraic structure that makes them vulnerable to "
    "bit-by-bit attacks. This is why most serious cryptographic operations use prime moduli."
)

pdf.section("7. Summary")
pdf.body(
    "This challenge featured an RSA system where two key pairs shared related primes. "
    "The primes of the second key were derived from the first key's primes using XOR of "
    "modular exponentiations. Because XOR is a bitwise operation, we could recover the "
    "original primes one bit at a time using a technique called 2-adic lifting.\n\n"
    "The attack required:\n"
    "  1. Understanding the bitwise nature of XOR\n"
    "  2. Recognizing that mod 2^b arithmetic is \"local\" (low bits only depend on low bits)\n"
    "  3. Building p1 from LSB to MSB, pruning with both N1 and N2 constraints\n"
    "  4. Scanning for the unknown iteration index k\n\n"
    "Runtime: ~5 minutes on a modern laptop.\n\n"
    "Flag: CSCPT{d0nt_us3_rel4ted_pr1mes}"
)

# ─── Save ───
out_path = "/Users/ctw03464/Documents/CTF/yamole/challs/crypto/hard/xor-prime/writeup.pdf"
pdf.output(out_path)
print(f"PDF written to {out_path}")
