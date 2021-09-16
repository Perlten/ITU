// Advanced Programming, Exercises by A. Wąsowski, IT University of Copenhagen
//
// Work on this file by following the associated exercise sheet
// (available in PDF in the same directory).
//
// The file is meant to be compiled inside sbt, using the 'compile' command.
// To run the compiled file use the 'run' or 'runMain'.
// To load the file int the REPL use the 'console' command.
//
// Continue solving exercises in the order presented in the PDF file. The file
// shall always compile, run, and pass tests (for the solved exercises),
// after you are done with each exercise (if you do them in order).
// Compile and test frequently. Best continously.

package fpinscala

object Perlt {
  def main(args: Array[String]): Unit = {}
}

object Exercises extends App with ExercisesInterface {

  import fpinscala.List._

  // Exercise 1 requires no programming

  def tail[A](as: List[A]): List[A] = {
    as match {
      case Nil              => throw new Exception()
      case Cons(head, tail) => tail
    }
  }

  // Exercise 3

  // @annotation.tailrec
  // Uncommment the annotation after solving to make the
  // compiler check whether you made the solution tail recursive
  def drop[A](l: List[A], n: Int): List[A] = {
    (l, n) match {
      case (Nil, _)              => throw new Exception()
      case (_, 0)                => l
      case (Cons(head, tail), _) => drop(tail, n - 1)
    }
  }

  // Exercise 4

  def dropWhile[A](l: List[A], f: A => Boolean): List[A] = {
    l match {
      case Nil              => Nil
      case Cons(head, tail) => if (f(head)) dropWhile(tail, f) else l
    }
  }

  // Exercise 5
  def init[A](l: List[A]): List[A] = {
    l match {
      case Nil              => throw new Exception()
      case Cons(head, Nil)  => Nil
      case Cons(head, tail) => Cons(head, init(tail))
    }
  }

  // Exercise 6

  def length[A](as: List[A]): Int = {
    as match {
      case Nil              => 0
      case Cons(head, tail) => List.foldRight(as, 0)((a, z) => z + 1)
    }
  }

  // Exercise 7

  // Uncommment the annotation after solving to make the
  // compiler check whether you made the solution tail recursive
  @annotation.tailrec
  def foldLeft[A, B](as: List[A], z: B)(f: (B, A) => B): B = {
    as match {
      case Nil              => z
      case Cons(head, tail) => foldLeft(tail, f(z, head))(f)
    }
  }

  // Exercise 8

  def product(as: List[Int]): Int = {
    as match {
      case Nil              => 1
      case Cons(head, tail) => List.foldRight(as, 1)(_ * _)
    }
  }

  def length1[A](as: List[A]): Int = {
    as match {
      case Nil              => 0
      case Cons(head, tail) => foldLeft(as, 0)((z, a) => z + 1)
    }
  }

  // Exercise 9
  def reverse[A](as: List[A]): List[A] = {
    as match {
      case Nil              => Nil
      case Cons(head, tail) => foldLeft(as, List[A]())((z, a) => Cons(a, z))
    }
  }

  // Exercise 10
  def foldRight1[A, B](as: List[A], z: B)(f: (A, B) => B): B = {
    as match {
      case Nil              => z
      case Cons(head, tail) => foldLeft(reverse(as), z)((b: B, a: A) => f(a, b))
    }
  }

  // Exercise 11

  def foldLeft1[A, B](as: List[A], z: B)(f: (B, A) => B): B = {
     foldRight(as, (b:B) => b)((a,g) => b => g(f(b,a)))(z)
  }

  // Exercise 12

  def append[A](a1: List[A], a2: List[A]): List[A] = a1 match {
    case Nil        => a2
    case Cons(h, t) => Cons(h, append(t, a2))
  }

  def concat[A](as: List[List[A]]): List[A] = {
    as match {
      case Nil              => Nil
      case Cons(head, tail) => foldLeft(tail, head)((b, a) => append(b, a))
    }
  }

  // Exercise 13

  def filter[A](as: List[A])(p: A => Boolean): List[A] = {
    as match {
      case Nil => Nil
      case Cons(head, tail) =>
        foldRight1(as, List[A]())((a, z) => if (p(a)) Cons(a, z) else z)
    }
  }

  // Exercise 14

  def flatMap[A, B](as: List[A])(f: A => List[B]): List[B] = {
    as match {
      case Nil => Nil
      case Cons(head, tail) =>
        List.foldRight(as, List[B]())((a, z) => append(f(a), z))
    }
  }

  // Exercise 15

  def filter1[A](l: List[A])(p: A => Boolean): List[A] = {
    l match {
      case Nil => Nil
      case Cons(head, tail) =>
        flatMap(l)((a) => if (p(a)) Cons(a, Nil) else List[A]())
    }
  }

  def add(l: List[Int])(r: List[Int]): List[Int] = {
    (l, r) match {
      case (Cons(l_head, l_tail), Cons(r_head, r_tail)) =>
        zipWith((a: Int, b: Int) => a + b)(l, r)
      case (Nil, Nil) => Nil
      case (_, _)     => Nil
    }
  }
  // Exercise 17

  def zipWith[A, B, C](f: (A, B) => C)(l: List[A], r: List[B]): List[C] = {
    (l, r) match {
      case (Cons(l_head, l_tail), Cons(r_head, r_tail)) =>
        Cons(f(l_head, r_head), zipWith(f)(l_tail, r_tail))
      case (Nil, Nil) => Nil
      case (_, _)     => Nil
    }
  }
  // Exercise 18

  def hasSubsequence[A](sup: List[A], sub: List[A]): Boolean = {
    (sup, sub) match {
      case (_, Nil)              => true
      case (Nil, _)              => false
      case (Cons(l_head, l_tail), Cons(r_head, r_tail))  => if (l_head == r_head) hasSubsequence(l_tail, r_tail) else hasSubsequence(l_tail, sub)
    }
  }

}
