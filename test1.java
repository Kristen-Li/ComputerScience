  public static void main(String args[])

    {   int n = 9;
        String string = "Geeks11forGeeks";
        String out = "";
        char[] c = string.toCharArray();
        boolean reverse = true;

        String num = "";
        boolean isPrevInt = false;

        for (int i = 0; i < c.length(); i++) {
            if (!Character.isDigit(c[i])){
                if (isPrevInt) {
                    int foo = Integer.parseInt(num);
                    foo += n;
                    num = Integer.toString(foo);
                    if(reverse){
                        StringBuilder numReversed = new StringBuilder(num);
                        numReversed.reverse();
                        String num2 = numReversed.toString();
                        int num3= Integer.parseInt(num2);
                        out += Integer.toString(num3);
                    } else {
                        out += Integer.toString(num);
                    }

                    num = "";
                }
                out += Character.toString(c[i]);
                isPrevInt = false;
            }
            else {
//                num can be char[]. Easier for reverse?
                num += Character.toString(c[i]);
                isPrevInt = true;
            }
        }

        System.out.println(out);

    }
