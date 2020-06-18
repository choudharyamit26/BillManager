# Program to input a number upto 5 digits and print it in words
def num_to_word(digit):
    number = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    nty = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninty"]
    tens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
            "Nineteen"]
    # n = int(input("Enter a number "))
    if digit > 99999:
        print("Cant solve for more than 5 digits")
    else:
        d = [0, 0, 0, 0, 0]
        i = 0
        while digit > 0:
            d[i] = digit % 10
            i += 1
            digit = digit // 10
        num = ""
        if d[4] != 0:
            if (d[4] == 1):
                num += tens[int(d[3])] + " Thousand "
            else:
                num += nty[int(d[4])] + " " + number[int(d[3])] + " Thousand "
        else:
            if d[3] != 0:
                num += number[int(d[3])] + " Thousand "
        if d[2] != 0:
            num += number[int(d[2])] + " Hundred "
        if d[1] != 0:
            if (d[1] == 1):
                num += tens[int(d[0])]
            else:
                num += nty[int(d[1])] + " " + number[int(d[0])]
        else:
            if d[0] != 0:
                num += number[int(d[0])]
        return num + " Only "


# x = num_to_word(59687)
# print(x)
