# PCPP

# Exercise 1.1

## 1 The chance of getting 20_000_000 is slim to none. This is caused by the data race to access count, caused by the non-deterministic approach of the scheduler.

## 2 Now there are a good chance of hitting 200. This is because the scheduler needs time to start up a second thread. During this time the first thread has already reached the limit of 100. However, it is not a guarantee that this will occur every time because of the nature of the non-deterministic scheduler.

## 3 When the compiler compiles i++, i = i + 1 or i += 1 it ends up being the same machine code. Therefore, there is no difference whether you use one or the other.

## 4 Previously we had no control over the interleaving of the scheduler, now however we know that a certain operation happens-before another. This ensures that no race condition(data race) can happen since only one thread can write to the shared memory. This section of the code where data is written is called the critical section, and should be the focus when deciding how locks should be utilized.

## 5

```
public void testIpp();
Code:
0: aload_0
1: dup
2: getfield #1 // Field i:I
5: iconst_1
6: iadd
7: putfield #1 // Field i:I
10: return

public void testIPE1();
Code:
0: aload_0
1: dup
2: getfield #1 // Field i:I
5: iconst_1
6: iadd
7: putfield #1 // Field i:I
10: return

public void testIEIP1();
Code:
0: aload_0
1: aload_0
2: getfield #1 // Field i:I
5: iconst_1
6: iadd
7: putfield #1 // Field i:I
10: return

No matter the approach it compiles to the same.
2: getfield #1 // Field i:I
5: iconst_1
6: iadd
7: putfield #1 // Field i:I
```

Even if i++ might seem like a atomic operation, it consists of three. Read the field, increment the field, overwrite the field with the new value.

It is because the operation is not atomic that race conditions (data-race) can occur.

## 6 Because one thread now use decrement the counter without a lock, we encounter a race condition. We observe in all runs ends with a value of below zero. I believe this is the case because even if thread one does not have to wait for another thread to release the lock (since no other thread currently ever claims it) it still creates an overhead that results in the counter being below zero in every run.

When the lock is also used to decrement the counter, it eliminates the race condition. This is a result of the critical section being encapsulated, therefore the scheduler executes it in the same interleaving.

## 7 Happens-before indicates a guarantee that certain operations have been executed before other operations runs. This is done be forcing the JVM and more precisely its scheduler how it should order its interleaving.

# Exercise 1.2

## 1

## 2 This can happen if the scheduler creates an interleaving that looks like this

Thread 1:

```
 System.out.println("-");
```

Thread 2:

```
 System.out.println("-");
```

Thread 1:

```
 try {
      Thread.sleep(50);
    } catch (Exception e) {
    }
    System.out.println("|");
```

Thread 2:

```
 try {
      Thread.sleep(50);
    } catch (Exception e) {
    }
    System.out.println("|");
```

There are however many possible combinations that will create an undesired outcome, and since the scheduler is non-deterministic we have no control over how the interleaving is managed.

## 3 Since we now have put the critical section inside a lock, we ensure that no race condition can appear. This is done by ensuring that the critical section is run in the same interleaving.



## 4 TODO


# Exercise 1.3


