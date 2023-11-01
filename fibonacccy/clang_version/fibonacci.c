int fibo_recursive(int length) {
    if (length <= 1) {
        return length;
    }

    return fibo(length - 1) + fibo(length - 2);
}


int fibo_iter(int length) {
    if (length <= 1) {
        return length;
    }

    int a = 0;
    int b = 1;
    int fib;

    for (int i = 2; i <= length; i++) {
        fib = a + b;
        a = b;
        b = fib;
    }

    return fib;
}

void matrix_multiply(unsigned long long a[2][2], unsigned long long b[2][2], unsigned long long result[2][2]) {
    unsigned long long x = a[0][0] * b[0][0] + a[0][1] * b[1][0];
    unsigned long long y = a[0][0] * b[0][1] + a[0][1] * b[1][1];
    unsigned long long z = a[1][0] * b[0][0] + a[1][1] * b[1][0];
    unsigned long long w = a[1][0] * b[0][1] + a[1][1] * b[1][1];
    
    result[0][0] = x;
    result[0][1] = y;
    result[1][0] = z;
    result[1][1] = w;
}

unsigned long long fibo_matrix_exponential(unsigned long long n) {
    if (n == 0) {
        return 0;
    }
    
    unsigned long long a[2][2] = {{1, 1}, {1, 0}};
    unsigned long long result[2][2] = {{1, 0}, {0, 1}};
    unsigned long long b[2][2];
    
    unsigned long long m = n - 1;
    while (m > 0) {
        if (m % 2 == 1) {
            matrix_multiply(result, a, b);
            for (int i = 0; i < 2; i++) {
                for (int j = 0; j < 2; j++) {
                    result[i][j] = b[i][j];
                }
            }
        }
        matrix_multiply(a, a, b);
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                a[i][j] = b[i][j];
            }
        }
        m /= 2;
    }
    
    return result[0][0];
}
