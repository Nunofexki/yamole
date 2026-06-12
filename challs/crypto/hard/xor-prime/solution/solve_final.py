from Crypto.Util.number import long_to_bytes

N1 = 77137069831818123807240774455950762767990413325793081508796360074912208684339628161427112820137604616364186817176929993166466430299619327344839882959001778451976753130205161851644854971151184622288638220974680166268249857500769241729148277129587383819591524571367295361146774816348936950289496781361622256443
N2 = 55257329876079913937467084112475373468177837748963935362332129789188857251800735356477517079143122141243407612092463419931588040889749099379431584939272391476247635032695559436249310025090918669634248311971318181756993765733583162339376948866195670567135163930175076492693764349661549726851793474969488819593
c = 58959278743937645851591382013760401753597451260953131216575517675841718487159634471812668046351886525599630606387992905969772305222532702273231458327776967101408551179284607382197009749321799536216946680372930943058129425282269200256091649631261562777705067403257726012903538791238687317454630715539764538584
e = 65537
BITS_MOD = 2**512
k_val = 210
l_val = 228

print(f"Solving with k={k_val}, l={l_val}")

candidates = [1]
for b in range(2, 513):
    mod = 1 << b
    n1_mod = N1 % mod
    n2_mod = N2 % mod
    new_candidates = []
    
    for p1_low in candidates:
        for bit in [0, 1]:
            p1_try = p1_low + bit * (1 << (b - 1))
            q1_try = (n1_mod * pow(p1_try, -1, mod)) % mod
            
            p1_k = pow(p1_try, k_val, mod)
            q1_k = pow(q1_try, k_val, mod)
            p2_mod = ((p1_k ^ q1_k) + 1) % mod
            
            p1_l = pow(p1_try, l_val, mod)
            q1_l = pow(q1_try, l_val, mod)
            q2_mod = ((p1_l ^ q1_l) + 1) % mod
            
            if (p2_mod * q2_mod) % mod == n2_mod:
                new_candidates.append(p1_try)
    
    candidates = new_candidates
    if b % 64 == 0:
        print(f"  bit {b}: {len(candidates)} candidates")
    if not candidates:
        print(f"  DIED at bit {b}")
        break

print(f"\nFinal: {len(candidates)} candidates")
print("Checking which divide N1...")

for p1 in candidates:
    if N1 % p1 == 0:
        q1 = N1 // p1
        print(f"\nFOUND p1 = {p1}")
        print(f"q1 = {q1}")
        
        p2 = (pow(p1, k_val, BITS_MOD) ^ pow(q1, k_val, BITS_MOD)) + 1
        q2 = (pow(p1, l_val, BITS_MOD) ^ pow(q1, l_val, BITS_MOD)) + 1
        print(f"N2 check: {p2 * q2 == N2}")
        
        phi = (p1 - 1) * (q1 - 1)
        d = pow(e, -1, phi)
        flag = long_to_bytes(pow(c, d, N1))
        print(f"Flag: {flag}")
        break
else:
    print("No candidate divides N1!")
