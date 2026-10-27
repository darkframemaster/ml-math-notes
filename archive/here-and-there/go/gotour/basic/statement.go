package main

import (
    "fmt"
    "math"
    "time"
    "runtime"
)

func sum_to_hundred(){
    sum := 0
    for i := 0 ; i < 100 ; i ++ {
        sum += i
    }
    fmt.Println(sum)
}

func sum_to_sum(){
    sum := 1
    for ; sum < 100; {
        sum += sum
    }
    fmt.Println(sum)
    // golang has no while statement, but you can write a while statement 
    // use for statement.
    for sum < 1000 {
        sum += sum
    }
    fmt.Println(sum)
}

func dead_loop(){
    fmt.Println("Press Ctr+c to end.")
    for {
    }
}

func sqrt(x float64) string{
    if x < 0{
        return sqrt(-x) + "i"
    }
    return fmt.Sprint(math.Sqrt(x))
}

func pow(x, n, lim float64) float64 {
    if v := math.Pow(x, n); v < lim {
        return v
    } else {
        fmt.Printf("%g >= %g\n", v, lim)
    }
    return lim
}


func switch_statement() {
    fmt.Print("Go runs on: ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("OS X.")
    case "linux":
        fmt.Println("Linux.")
    default:
        fmt.Printf("%s.", os)
    }

    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("Good morning!")
    case t.Hour() < 17:
        fmt.Println("Good afternoon.")
    default:
        fmt.Println("Good evening.")
    }
}

func defer_statement(){
    // Defer use a STACK structure: first in last out
    defer fmt.Print("hello darkframexue\n")
    defer fmt.Print(" & ")
    defer fmt.Print("world")

    fmt.Print("hello")
}


func main(){
    sum_to_hundred()
    sum_to_sum()
    fmt.Println(sqrt(2), sqrt(-4))
    switch_statement()
    defer_statement()
    dead_loop()
}
