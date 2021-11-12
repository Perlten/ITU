// wasowski, Advanced Programming, IT University of Copenhagen
package fpinscala.laziness
import scala.language.higherKinds

import org.scalacheck.Gen
import org.scalacheck.Arbitrary
import org.scalacheck.Arbitrary.arbitrary

import stream00._ // uncomment to test the book solution (should pass your tests)
import scala.util.Random
// import stream01._ // uncomment to test the broken headOption implementation
// import stream02._ // uncomment to test another version that breaks headOption

class StreamSpec
    extends org.scalatest.freespec.AnyFreeSpec
    with org.scalatest.matchers.should.Matchers
    with org.scalatestplus.scalacheck.ScalaCheckPropertyChecks {

  import Stream._

  // A simple converter of lists to streams

  def list2stream[A](la: List[A]): Stream[A] =
    la.foldRight(Stream.empty[A])(cons[A](_, _))

  // There  is  a name  clash  between  Stream.empty and  the  testing
  // library, so we need to qualify Stream.empty

  // An example generator  of random finite non-empty  streams (we use
  // the  built in  generator of  lists and  convert them  to streams,
  // using the above converter)
  //
  // 'suchThat'  filters  out  the  generated instances  that  do  not
  // satisfy the predicate given in the right argument.

  def genNonEmptyStream[A](implicit arbA: Arbitrary[A]): Gen[Stream[A]] =
    for {
      la <- arbitrary[List[A]] suchThat { _.nonEmpty }
    } yield list2stream(la)

  def genNonNegativeInt[A](): Gen[Int] = {
    Gen.choose[Int](1, Int.MaxValue)
  }

  implicit val arbIntStream =
    Arbitrary[Stream[Int]](genNonEmptyStream[Int])

  "headOption" - {

    // Exercise 1 (no coding, understand)

    // A scenario test:

    "returns None on an empty Stream (01)" in {

      Stream.empty.headOption shouldBe (None)
    }

    // Two property tests:

    "returns the head of a singleton stream packaged in Some (02)" in {

      forAll { (n: Int) =>
        cons(n, Stream.empty).headOption should be(Some(n))
      }
    }

    "returns the head of random stream packaged in Some (02)" in {

      // Make the generator available in the context
      // implicit val arbIntStream =
      //   Arbitrary[Stream[Int]](genNonEmptyStream[Int])

      // Uses our generator of non empty streams
      // thanks to the implicit declaration above
      forAll { (s: Stream[Int]) =>
        s.headOption shouldNot be(None)
      }
    }

    // Exercise 2 (add here)
    //
    // ...

    "whatever" in {
      forAll { (s: Stream[Int]) =>
        noException shouldBe thrownBy(
          cons(1, cons(throw new Exception, s)).headOption
        )
      }

    }

  }

  "take" - {

    "takes does force the head nor tail" in {
      forAll { (s: Stream[Int]) =>
        val x = cons(
          throw new Exception,
          cons(throw new Exception, cons(throw new Exception, s))
        )
        x.take(10)
      }
    }

    "takes(n) does not force n + 1" in {
      forAll { (s: Stream[Int]) =>
        val x = cons(
          0,
          cons(1, cons(2, cons(throw new Exception, s)))
        )
        x.take(3).forAll(e => true) shouldBe (true)
      }
    }

    "exercise 5" in {
      implicit val arbInt = Arbitrary[Int](genNonNegativeInt())

      forAll("s", "n") { (s: Stream[Int], n: Int) =>
        s.take(n).take(n).toList shouldBe s.take(n).toList
      }
    }
  }

  "drop" - {
    "exercise 6" in {
      implicit val arbInt = Arbitrary[Int]({
        Gen.choose[Int](1, (Int.MaxValue - 10) / 2)
      })

      forAll("s", "n", "m") { (s: Stream[Int], n: Int, m: Int) =>
        s.drop(n).drop(m).toList shouldBe s.drop(n + m).toList
      }
    }

    "exercise 7" in {
      implicit val arbInt = Arbitrary[Int](genNonNegativeInt())

      forAll("s", "n") { (s: Stream[Int], n: Int) =>t
        val s2 = s.append(s.take(n).map(e => throw new Exception))
        noException shouldBe thrownBy(s2.drop(n).toList)
      }
    }
  }

  "map" - {
    "exercise 8" in {
      forAll("s") { (s: Stream[Int]) =>
        val s2 = s.map(e => identity(e))
        s.toList shouldBe (s2.toList)
      }
    }

    "exercise 9" in {
      val s = Stream.fibs
      s.map(e => e)
      noException shouldBe thrownBy(s.map(e => e))
    }

  }

  "append" - {

    "exercise 10" in {
      forAll("s") { (s: Stream[Int]) =>
        val n = Random.between(0, s.toList.length + 1)

        val streamToAppend = s.take(n).map(e => 1)
        val appendedStream = streamToAppend.append(s)

        streamToAppend.toList shouldBe(appendedStream.take(n).toList)
      }
    }

  }

}
