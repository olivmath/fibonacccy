int fibo(int length) {
    if (length <= 1) {
        return length;
    }

    return fibo(length - 1) + fibo(length - 2);
}
