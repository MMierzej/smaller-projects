using System;
using System.Collections;
using System.Collections.Generic;


public class Linked<T> : IListCollection<T> where T : IComparable<T> {
    protected class Node {
        public T Value { get; set; }
        public Node Next { get; set; }

        public Node(T val) {
            Value = val;
            Next = null;
        }
    }
    Node head;
    bool empty = true;
    int len;
    public int Length {
        get {
            return len;
        }
    }

    public bool IsEmpty() { return empty; }

    public void Add(T value) {
        if (empty) {
            head = new Node(value);
            empty = false;
        }
        else {
            Node aux = head;
            while (aux.Next != null) aux = aux.Next;
            aux.Next = new Node(value);
        }

        len++;
    }

    public void Insert(int index, T value) {
        if (index >= Length || index < 0) {
            Console.WriteLine("Insert: Index out of bounds.");
        } else {
            Node aux = head;

            for (int i = 0; i < index; i++) {
                aux = aux.Next;
            }

            aux.Value = value;
            len++;
        }

    }

    public void Remove(T value) {
        if (empty) return;
        Node prev = null;
        Node aux = head;

        while (aux != null) {
            if (aux.Value.Equals(value)) {
                if (aux == head) {
                    head = aux.Next;
                    aux.Next = null;
                    empty = true;
                } else {
                    prev.Next = aux.Next;
                    aux.Next = null;
                }
                len--;
                return;
            }
            prev = aux;
            aux = aux.Next;
        }

    }

    public void RemoveAt(int index) {
        if (empty) return;
        if (index >= Length || index < 0) {
            Console.WriteLine("RemoveAt: Index out of bounds.");
        } else {
            Node prev = null;
            Node aux = head;

            for (int i = 0; i < index; i++) {
                prev = aux;
                aux = aux.Next;
            }

            if (aux == head) {
                head = aux.Next;
                aux.Next = null;
                empty = true;
            } else {
                prev.Next = aux.Next;
                aux.Next = null;
            }
            len--;
        }

    }

    public T Get(int index) {
        if (index >= Length || index < 0) {
            Console.WriteLine("Get: Index out of bounds.");
        } else {
            Node aux = head;

            for (int i = 0; i < index; i++) {
                aux = aux.Next;
            }

            return aux.Value;
        }

        return default(T);
    }
}