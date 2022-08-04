using System;
using System.Text;
using System.Collections;
using System.Collections.Generic;

public class Lista<T> : IListCollection<T>, IEnumerable<T>, IEnumerator<T> where T : IComparable<T> {
    protected class Node {
        Node next;
        Node prev;
        public T Value { get; set; }

        public Node(T value) {
            Value = value;
            next = null;
            prev = null;
        }

        public void set_next(Node node) {
            next = node;
        }

        public Node get_next() {
            return next;
        }

        public void set_prev(Node node) {
            prev = node;
        }

        public Node get_prev() {
            return prev;
        }
    }

    protected Node front;
    protected Node back;
    protected Node curr;
    protected Node next_curr;
    protected bool empty = true;
    protected int len;

    public Lista() {
        front = back = curr = null;
        len = 0;
    }

    public int Length {
        get { return len; }
    }

    public bool IsEmpty() {
        return empty;
    }

    public T this[int index] {
        get {
            if (index >= len || index < 0) {
                Console.WriteLine("get: Index out of bounds.");
                return default(T);
            }
            Reset();
            for (int i = 0; i < index; i++) curr = curr.get_next();
            return curr.Value;
        }

        set {
            if (index >= len || index < 0) {
                Console.WriteLine("set: Index out of bounds.");
                return;
            }
            Reset();
            for (int i = 0; i < index; i++) curr = curr.get_next();
            curr.Value = value;
        }
    }

    public void Add(T value) {
        Node node = new Node(value);

        if (empty) {
            front = node;
            back = node;
            empty = false;
        } else {
            front.set_next(node);
            node.set_prev(front);
            front = node;
        }

        len++;
    }

    public void Insert(int index, T value) {
        if (index >= len || index < 0) {
            Console.WriteLine("Insert: Index out of bounds.");
            return;
        }

        T dummy = this[index]; // now curr points at the correct Node
        curr.Value = value;
    }

    void pop_front() {
        if (empty) return;

        T val = front.Value;

        if (front.get_prev() == null) {
            empty = true;
            front = null;
            back = null;
        } else {
            front = front.get_prev();
            front.get_next().set_prev(null);
            front.set_next(null);
        }
    }

    void pop_back() {
        if (empty) return;

        T val = back.Value;

        if (back.get_next() == null) {
            empty = true;
            front = null;
            back = null;
        } else {
            back = back.get_next();
            back.get_prev().set_next(null);
            back.set_prev(null);
        }
    }

    public void Remove(T value) {
        Reset();

        while (curr != null) {
            if (curr.Value.Equals(value)) {
                if (curr == back) pop_back();
                else if (curr == front) pop_front();
                else {
                    curr.get_prev().set_next(curr.get_next());
                    curr.get_next().set_prev(curr.get_prev());
                    curr.set_next(null);
                    curr.set_prev(null);
                }
                len--;
                return;
            }

            curr = curr.get_next();
        }
    }

    public void RemoveAt(int index) {
        if (index >= len || index < 0) {
            Console.WriteLine("RemoveAt: Index out of bounds.");
            return;
        }

        T dummy = this[index]; // now curr points at the needed element

        if (curr == back) pop_back();
        else if (curr == front) pop_front();
        else {
            curr.get_prev().set_next(curr.get_next());
            curr.get_next().set_prev(curr.get_prev());
            curr.set_next(null);
            curr.set_prev(null);
        }
        len--;
    }

    public T Get(int index) {
        return this[index];
    }

    IEnumerator IEnumerable.GetEnumerator() {
        Reset();
        return (IEnumerator) GetEnumerator();
    }

    public IEnumerator<T> GetEnumerator() {
        Reset();
        return (IEnumerator<T>) this;
    }

    public T Current => curr.Value;
    object IEnumerator.Current => Current;

    public bool MoveNext() {
        curr = next_curr;

        if (curr != null) {
            next_curr = curr.get_next();
            return true;
        }

        return false;
    }

    public void Reset() {
        curr = back;
        next_curr = back;
    }

    public void Dispose() {}

    public override string ToString() {
        StringBuilder sb = new StringBuilder("[");
        bool first = true;

        foreach (T x in this) {
            if (first) {
                sb.AppendFormat("{0}", x);
                first = false;
            } else sb.AppendFormat(", {0}", x);
        }

        sb.Append("]");
        return sb.ToString();
    }
}
