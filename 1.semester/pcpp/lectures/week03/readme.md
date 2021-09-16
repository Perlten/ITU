# Lecture 3: Performance measurements

## Goals

The goals of this lecture are:
* Motivate the need for performance measurements
* Show benchmarks for a number of Java concepts including: some math functions, object creation, threads, 
    a sorting algorithm and an algorithm for computing prime factors
* Introduce the statistics of benchmarking (normal distribution, mean and variance).
* Make you aware off some pitfalls when using floating point numbers

## Readings 

* The note by Peter Sestoft: [Microbenchmarks in Java and C sharp](https://github.itu.dk/jst/PCPP2021-public/blob/master/week03/benchmarkingNotes.pdf)
that can be found in the GitHub folder with course material for week 3

You may skip sections 9-12.

## To do before lecture 3
During lecture 3 you will be asked to do some experiments on your own computer. 
In order to do that you need to do:

* clone the directory Exercises (same folder as this file)
* test that you can run ` Measurement.java ` (in this subdirectory ` week03/exercises/app/src/main/java/exercises03 `)
for example by executing:

 ` gradle -PmainClass=exercises03.Measurement run `

Make sure you can also run   ` timingMultiplication.java `

### Optional readings
* The pitfalls of using floating point numbers: 

 * David Goldberg [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://github.itu.dk/jst/PCPP2021-public/blob/master/week03/IEEE754_article.pdf)


## Lecture slides
Could be updated, so please check that you have the latest version

[lecture03.pdf (last update September 12, 2021)](https://github.itu.dk/jst/PCPP2021-public/blob/master/week03/Lecture03.pdf)


## Exercises

[exercises03.pdf](updated September 10)(https://github.itu.dk/jst/PCPP2021-public/blob/master/week03/exercises03.pdf)
