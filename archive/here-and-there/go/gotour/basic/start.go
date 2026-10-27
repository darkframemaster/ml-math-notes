// Every go program is a package,the start point is the 'main' package
package main

/* 
 Import part, you can also write this part like:

    import "fmt"
    import "math"

 Package name is the last directory of the path. 
 Ex: if you want to use package "math/rand", start with "rand".
*/
import (
    "fmt"
    "math"
    "math/rand"
    "math/cmplx"
)

/*
 If params are the same type, you can only declare the type of the
 lastest param,

    func add(x, y int) int{
        return x + y
    }
*/
func add(x int, y int) int {
    return x + y
}

func swap(x, y string) (string, string){
    return y, x
}

func split(sum int)(x, y int){
    x = sum * 4 / 9
    y = sum - x
    return
}

var c, python, java string = "c", "python", "java"
var name string
var age int
// CANNOT USE: var name string, age int
var (
    ToBe   bool       = false
    MaxInt uint64     = 1 << 64 - 1
    z      complex128 = cmplx.Sqrt(-5 + 12i)
)

func variable(){
    // Inside function you can declare a variable like this
    // but outside function, you can only use key word variable
    gender := "male"
    c, python, java := true, false, "no!"
    var name string = "darkframexue"

    types := "bool, string,"
    int_types  := "int int8 int16 int32 int64"
    // unsigned int
    uint_types := "uint uint8 uint16 uint32 uint64 uintptr"

    alias_types := "byte //uint8\nrune  //int32\n"
    float_types := "float32 float64"
    complex_types := "complex64 complex128"
    fmt.Println(gender, c, python, java, name, types, int_types, uint_types, alias_types, float_types, complex_types)
}

func check_type(){
    const f = "%T(%v)\n"
    fmt.Printf(f, ToBe, ToBe)
    fmt.Printf(f, MaxInt, MaxInt)
    fmt.Printf(f, z, z)
}

func default_value(){
    var i int
    var f float64
    var b bool
    var s string
    fmt.Printf("%v, %v, %v, %q\n", i, f, b, s)
}

func type_convert(){
    i := 42
    f := float64(i)
    u := uint(f)
    fmt.Printf("%v, %v, %v", i, f, u)
}

func const_variable(){
    // CANNOT declare a const variable use :=
    const Word = "世界"
    fmt.Println("Hello", Word)
}

const (
    Big   = 1 << 100
    Small = Big >> 99
)
func needInt(x int) int {return x * 10 + 1}
func needFloat(x float64) float64 {return x * 0.1}
func const_number(){
    // MAX INT value is 64 bit
    //fmt.Println(needInt(Big))
    fmt.Println(needInt(Small))
    fmt.Println(needFloat(Small))
    fmt.Println(needFloat(Big))
}

func main(){
    rand.Seed(4)
    fmt.Println("My favorite number is", rand.Intn(10))
    fmt.Println(math.Pi)
    fmt.Println(add(42, 13))
    fmt.Println(swap("hello", "world"))
    fmt.Println(split(17))

    check_type()
    default_value()
    const_variable()
}
