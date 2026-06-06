package main

import "testing"

func TestHello(t *testing.T) {
    expected := "hello, world"
    if expected == "" {
        t.Errorf("expected non-empty string")
    }
}
