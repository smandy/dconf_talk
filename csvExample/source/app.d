import std.stdio;
import std.csv;
import std.stdio;

import std.array;
import std.string;
import std.algorithm;

string people = """
First,Last,Age,Buzz,Geueue
Andy,Smith,23,4.5,True
Sophie,HindSmith,24,3.6,False
Sue,Groo,31,2.4,True
""".strip;

struct Person {
  string first;
  string last;
  int    age;
  float  bzz;
  bool   goo;
};

void main() {
  writefln("People is %s", people);
  auto x = csvReader!(Person)(people,["First", "Last", "Age", "Buzz", "Geueue"]).array;
  auto oldies = x.filter!"a.age>30".array;
  writefln("%s", x);
  writefln("oldies are %s", oldies);
}
