"""Local verification that the exploit logic works"""
from Crypto.Util.number import getRandomInteger
from Crypto.Hash import TupleHash128

GENERATOR = 0x2
Q = 4863582031353698198761328444493879228310321364281230162432941418974766035646994473626431630074195869892666977725902703437672528883791089201079706878830495677314851995801210780927161054477270449206302430992983000362680537603073911181954436112981857313308698944840733489877808410943336233052503234913545497471564833465501423042038660248491510385678358194559059271654320944019327351043166386768574242028957654775069955451796948455362239879097118518200743383781792266381988326107437550218806712025903303696479597447784386404544762534889281069284960359265592322943158476484143869956733696787606184300373875007099479039839737235636800602135437322790489431635178114950297146384525504411311985677915624022281816199470525512536884444099066124586374766347855189025988552225935417330198821849818515883717265006356649038533599313538003254211409511373248001631185015759679768429197412497657484402329229273463264931927078841128724273334163

def SchnorrVerify(h, u, c, z):
    if u * h * z % Q == 0:
        return False
    tuple_hash = TupleHash128.new(digest_bytes=400)
    tuple_hash.update(GENERATOR.to_bytes(400, "big"))
    tuple_hash.update(Q.to_bytes(400, "big"))
    tuple_hash.update(h.to_bytes(400, "big"))
    c_prime = int.from_bytes(tuple_hash.digest(), "big")
    hashes_match = c == c_prime
    valid_eq = pow(GENERATOR, z, Q) == u * pow(h, c, Q) % Q
    return hashes_match and valid_eq

# Simulate server
x = getRandomInteger(3071)
H = pow(GENERATOR, x, Q)
print(f"Server public key H generated (private key unknown to attacker)")

# ATTACKER: forge proof without knowing x
tuple_hash = TupleHash128.new(digest_bytes=400)
tuple_hash.update(GENERATOR.to_bytes(400, "big"))
tuple_hash.update(Q.to_bytes(400, "big"))
tuple_hash.update(H.to_bytes(400, "big"))
c = int.from_bytes(tuple_hash.digest(), "big")

z = 1337  # arbitrary
u = (pow(GENERATOR, z, Q) * pow(H, -c, Q)) % Q

# Verify
result = SchnorrVerify(H, u, c, z)
print(f"Forged proof accepted: {result}")
assert result, "Exploit failed!"
print("SUCCESS: Exploit works without knowing the private key!")
