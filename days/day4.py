from days import AOCDay, day

DEBUG = True

@day(4)
class Day4(AOCDay):
    test_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split("\n")
    test_input2 = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".split("\n")
    test_input3 = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""".split("\n")

    passports = []

    REQUIRED = {
        "byr": lambda x: int(x) and len(x) == 4 and 1920 <= int(x) <= 2002,
        "iyr": lambda x: int(x) and len(x) == 4 and 2010 <= int(x) <= 2020,
        "eyr": lambda x: int(x) and len(x) == 4 and 2020 <= int(x) <= 2030,
        "hgt": lambda x: x[:-2] != "" and int(x[:-2]) and x[-2:] in ["cm", "in"] and (
            (x[-2:] == "cm" and 150 <= int(x[:-2]) <= 193) or
            (x[-2:] == "in" and 59 <= int(x[:-2]) <= 76)
        ),
        "hcl": lambda x: x[0] == "#" and all(y in "1234567890abcdef" for y in x[1:]),
        "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
        "pid": lambda x: int(x) and len(x) == 9
    }

    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """

    def test(self, input_data):
        assert self.REQUIRED['byr']("2002") == True, f"byr '2002' should be valid but is not"
        assert self.REQUIRED['byr']("2003") == False, f"byr '2003' should be invalid but is not"
        assert self.REQUIRED['hgt']("60in") == True, f"hgt '60in' should be valid but is not"
        assert self.REQUIRED['hgt']("190cm") == True, f"hgt '190cm' should be valid but is not"
        assert self.REQUIRED['hgt']("190in") == False, f"hgt '190in' should be invalid but is not"
        assert self.REQUIRED['hgt']("60") == False, f"hgt '190' should be invalid but is not"
        assert self.REQUIRED['hcl']("#123abc") == True, f"hcl '#' should be valid but is not123abc"
        assert self.REQUIRED['hcl']("#123abz") == False, f"hcl '#' should be invalid but is not123abz"
        assert self.REQUIRED['hcl']("123abc") == False, f"hcl '123abc' should be invalid but is not"
        assert self.REQUIRED['ecl']("brn") == True, f"ecl 'brn' should be valid but is not"
        assert self.REQUIRED['ecl']("wat") == False, f"ecl 'wat' should be invalid but is not"
        assert self.REQUIRED['pid']("000000001") == True, f"pid '000000001' should be valid but is not"
        assert self.REQUIRED['pid']("0123456789") == False, f"pid '0123456789' should be invalid but is not"

    def common(self, input_data):
        self.passports = []
        input_data = ("\n".join(input_data)).split("\n\n")
        for passport in input_data:
            parts = (" ".join(passport.split("\n"))).split(" ")
            p = {}
            for part in parts:
                name, value = part.split(":")
                p[name] = value
            self.passports.append(p)

    def part1(self, input_data):
        valid = 0
        for passport in self.passports:
            for key, validator in self.REQUIRED.items():
                if key not in passport:
                    break
            else:
                valid += 1
        yield valid

    def part2(self, input_data):
        valid = 0
        for passport in self.passports:
            for key, validator in self.REQUIRED.items():
                if key not in passport:
                    break
                try:
                    if not validator(passport[key]):
                        break
                except ValueError:
                    break
            else:
                valid += 1
        yield valid
