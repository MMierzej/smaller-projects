#!/bin/bash

javac -d compiled/ *.java
javac -d compiled/ ./model/*.java
javac -d compiled/ ./view/*.java
javac -d compiled/ ./controller/*.java

cd compiled
java Main $1 $2