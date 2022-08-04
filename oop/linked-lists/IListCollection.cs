using System;

public interface IListCollection<T> where T : IComparable<T> {
    int Length {
        get;
    }
    bool IsEmpty();
    void Add(T value);
    void Insert(int index, T value);
    void Remove(T value);
    void RemoveAt(int index);
    T Get(int index);
}