using System;
using System.Collections;
using System.Collections.Generic;


public class Program {
    public static void Main() {
        Lista<double> list = new Lista<double>();

        Console.WriteLine("Długość listy: " + list.Length);
        list.Add(3.14159265);
        Console.WriteLine("Add...");
        Console.WriteLine("Pierwszy element: " + list[0]);
        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine("Usunięcie 3.1459265");
        list.Remove(3.1459265);
        Console.WriteLine("Pierwszy element: " + list[0]);
        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine("Usunięcie 3.14159265");
        list.Remove(3.14159265);
        Console.WriteLine("Długość listy " + list.Length);

        Console.WriteLine();
        Console.WriteLine("Dodanie 10 elementów...");
        for (int i = 0; i < 10; i++) {
            list.Add(3.14 + i);
        }
        Console.WriteLine(list);
        Console.WriteLine("list[1] = 0.25;");
        list[1] = 0.25;
        Console.WriteLine(list);
        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine();

        Console.WriteLine("Lista wypisana w foreach...");
        foreach(var x in list) {
            Console.WriteLine(x);
        }

        Console.WriteLine();
        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine("Usunięcie 10.14 i 20");
        list.Remove(10.14);
        list.Remove(20);
        Console.WriteLine("Lista wypisana w foreach...");
        foreach(var x in list) {
            Console.WriteLine(x);
        }
        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine();

        Console.WriteLine("Usunięcie z indeksu 0 5 razy z rzędu...");
        for (int i = 0; i < 5; i++) {
            list.RemoveAt(0);
        }
        Console.WriteLine("list[54] = 2.02;");
        list[54] = 2.02;
        Console.WriteLine("Lista wypisana w foreach...");
        foreach(var x in list) {
            Console.WriteLine(x);
        }
        Console.WriteLine();
        Console.WriteLine("Usunięcie z ostatniego indeksu...");
        list.RemoveAt(list.Length - 1);
        Console.WriteLine();
        Console.WriteLine("Lista wypisana w foreach...");
        foreach(var x in list) {
            Console.WriteLine(x);
        }
        Console.WriteLine();
        Console.WriteLine("Usunięcie pierwszego elementu 20 razy z rzędu...");
        for (int i = 0; i < 20; i++) {
            Console.Write(i + ". ");
            list.RemoveAt(0);
        }
        Console.WriteLine();
        Console.WriteLine("Lista wypisana w foreach...");
        foreach(var x in list) {
            Console.WriteLine(x);
        }
        Console.WriteLine();

        Console.WriteLine("Długość listy: " + list.Length);
        Console.WriteLine(list);

        Console.WriteLine();
        Console.WriteLine();
        Console.WriteLine();
        Console.WriteLine("Linked:");
        
        Linked<double> ll = new Linked<double>();
        Console.WriteLine("Add...");
        ll.Add(3.14);
        Console.WriteLine(ll.Get(0));
        ll.RemoveAt(0);
        Console.WriteLine("RemoveAt(0)");
        Console.WriteLine("IsEmpty(): " + ll.IsEmpty());
        Console.WriteLine("Długość: " + ll.Length);
        Console.WriteLine("Add...");
        ll.Add(3.14);
        Console.WriteLine(ll.Get(0));
        Console.WriteLine("IsEmpty(): " + ll.IsEmpty());
        Console.WriteLine("Długość: " + ll.Length);
        Console.WriteLine();

        for (int i = 0; i < 20; i++) {
            ll.Add(-i);
        }
        ll.Insert(10, 10);
        Console.WriteLine("ll[9]: " + ll.Get(9));
        Console.WriteLine("ll[10]: " + ll.Get(10));
        Console.WriteLine("IsEmpty(): " + ll.IsEmpty());
        Console.WriteLine("Długość: " + ll.Length);
    }
}