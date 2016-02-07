// http://stackoverflow.com/a/11994395/3177936

#pragma once

#define FE_1(WHAT, X) WHAT(X) 
#define FE_2(WHAT, X, ...) WHAT(X),FE_1(WHAT, __VA_ARGS__)
#define FE_3(WHAT, X, ...) WHAT(X),FE_2(WHAT, __VA_ARGS__)
#define FE_4(WHAT, X, ...) WHAT(X),FE_3(WHAT, __VA_ARGS__)
#define FE_5(WHAT, X, ...) WHAT(X),FE_4(WHAT, __VA_ARGS__)
//... repeat if needed

#define GET_MACRO(_1,_2,_3,_4,_5,NAME,...) NAME 
#define FOR_EACH(action,...) \
  GET_MACRO(__VA_ARGS__,FE_5,FE_4,FE_3,FE_2,FE_1,)(action,__VA_ARGS__)

#define VA_NUM_ARGS(...) VA_NUM_ARGS_IMPL(__VA_ARGS__, 5,4,3,2,1)
#define VA_NUM_ARGS_IMPL(_1,_2,_3,_4,_5,N,...) N

#define APPLY_TYPE(x) VarPyObject x
#define APPLY_TYPES(...) FOR_EACH(APPLY_TYPE, __VA_ARGS__)
#define PY_METHOD(x, ...) inline PyObject * x(APPLY_TYPES(__VA_ARGS__)) \
{\
    return this->call_python_method(#x, VA_NUM_ARGS(__VA_ARGS__), __VA_ARGS__);\
}

#define PY_ATTRIBUTE(x) inline PyObject * get_ ## x () \
{\
    return PyObject_GetAttrString(self, #x);\
}


// Class used to do 'automatic' creation of PyObjects when returning
// them to Python via PY_METHOD.
class VarPyObject
{
public:
    VarPyObject(const char* c)
    {
        this->obj = PyUnicode_FromString(c);
    }
    VarPyObject(PyObject* o)
    {
        this->obj = o;
    }
    PyObject * get_PyObject()
    {
        return obj;
    }
private:
    PyObject * obj;
};

class python_class
{
protected:
    python_class();
    python_class(PyObject *self);
    python_class(const python_class &); // Copy c'tor
    python_class &operator=(const python_class&); // Copy assignment
    virtual ~python_class();

    PyObject *call_python_method(const char *name, size_t count, ...);
    PyObject *self;
};
