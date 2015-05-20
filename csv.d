enum Species {
  PERSON, 
  DINOSAUR
};

string people = """
First,Last,Age,Species
Fred,Flintstone,35,PERSON
Wilma,Flintstone,32,PERSON
Barney,Rubble,30,PERSON
Betty,Rubble,28,PERSON
Pebbles,Flintstone,2,PERSON
Bambam,Rubble,1,PERSON
Dino,Flintstone,5,DINOSAUR
""".strip; // UFCS : x.strip() <=> strip(x);

struct Person {
  string first;
  string last;
  int    age;
  Species species;
};

void main() {
  writefln("People is %s", people);
  auto x = csvReader!(Person)(people,["First", "Last", "Age", "Species"]).array;
  auto oldies = x.filter!"a.age>20".array;
  writefln("%s", x);
  writefln("oldies are %s", oldies);
}
