// Andrzej Wąsowski, IT University of Copenhagen

object MyModule {

  def abs(n: Int): Int = if (n < 0) -n else n

  /* Exercise 1 */
  def square (n: Int): Int = ???

  private def formatAbs(x: Int) =
    s"The absolute value of $x is ${abs (x)}"

  val magic :Int = 42
  var result :Option[Int] = None

  def main(args: Array[String]): Unit = {
    f(10)
  }

  def f(n: Int): Int = {
    if (n == 0) {
      print(n)
      n
    }else {
      println(2*n)
      f(n-1)
    }
  }
}
