// For week 5
// raup@itu.dk 26/09/2021
package lecture05;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.stream.IntStream;

import java.util.concurrent.ThreadLocalRandom;

public class StreamExample {

    static String[] departments = {"CS", "DD", "BI"};
    
    public static void main(String[] args) throws FileNotFoundException {

	//Stream<Employee> employees = randomEmployees(); // Infinite stream using generate

	// Convert stream of employees to List
	List<Integer> l = randomEmployees()
	    .limit(50)
	    .map(Employee::getId)
	    .collect(Collectors.toList());

	// List of employees per department
	Map<String,List<Employee>> m = randomEmployees()
	    .limit(50)
	    .collect(Collectors.groupingBy(Employee::getDept));

	// Printing ids of all employees per department
	randomEmployees()
	    // .parallel()
	    .limit(50)
	    // .collect(Collectors.groupingByConcurrent(Employee::getDept))
	    .collect(Collectors.groupingByConcurrent(Employee::getDept))
	    .forEach((k,v) -> System.out.println(k+": "+v.stream().map(Employee::getId).collect(Collectors.toList()))); 


	
	// Printing salary per employee (employees retreived from file)
	String filename = "src/main/resources/employee-data.txt";
	BufferedReader reader = new BufferedReader(new FileReader(filename)); // Using lines() from BufferedReader	
	reader
	    .lines()
	    // .parallel()
	    .limit(10)
	    .map(s -> s.split(";"))
	    .map(i -> new Employee(Integer.parseInt(i[0]),
				   i[1],
				   Integer.parseInt(i[2])))
	    // .collect(Collectors.groupingByConcurrent(Employee::getId, Collectors.summingInt(Employee::getSalary)))
	    .collect(Collectors.groupingBy(Employee::getId, Collectors.summingInt(Employee::getSalary)))
	    .forEach((k,v) -> System.out.println(k+": "+v));
    }

    // Example of creating an infinite streams of employees
    static private Stream<Employee> randomEmployees() {
	return Stream.generate( () -> new Employee(ThreadLocalRandom.current().nextInt(10000),
						   departments[ThreadLocalRandom.current().nextInt(3)],
						   ThreadLocalRandom.current().nextInt(50000) ) );	
    }
}

class Employee {
    
    int id;
    String dept;
    int salary;
    
    public Employee(int id, String dept, int salary) {
	this.id     = id;
	this.dept   = dept;
	this.salary = salary;
    }

    public int getId() { return this.id; }

    public String getDept() { return this.dept; }

    public int getSalary() { return this.salary; }
    
}
