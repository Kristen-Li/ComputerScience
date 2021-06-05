public static void main(String args[]) {
        String string = "G33ks11forGeeks";
        StringBuilder out = new StringBuilder();
        int initialPosition = 2;
        int finalPosition = 3;
        HashMap<Character, String> map = new HashMap<Character, String>();

        // Add keys and values (number, number)
        map.put('0', "zero");
        map.put('1', "one");
        map.put('2', "two");
        map.put('3', "three");
        map.put('4', "four");
        map.put('5', "five");
        map.put('6', "six");
        map.put('7', "seven");
        map.put('8', "eight");
        map.put('9', "nine");

        char[] c = string.toCharArray();

        for (int i = 0; i < c.length; i++) {
            if (i < initialPosition -1 || i >= finalPosition) {
                out.append(c[i]);
            }
            else {
                if (Character.isDigit(c[i])){
                    out.append(map.get(c[i]));
                } else{
                    out.append(c[i]);
                }
            }
        }
        System.out.println(out);
    }
