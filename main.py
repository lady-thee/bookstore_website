from dataclasses import dataclass


@dataclass
class NewPerson:
    name: str
    age: int
    city: str


p = NewPerson("Nobara", 23, "japan")
print(p)
print(p.name, p.age)

print(hash(p))
