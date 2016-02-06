// http://stackoverflow.com/a/11994395/3177936
//
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


// Class used to do 'automatic' creation of PyObjects when returning
// them to Python via PY_METHOD.
class VarPyObject
{
public:
    VarPyObject(const char* c)
    {
        this->obj = PyUnicode_FromString(c);
    }
    PyObject * get_PyObject()
    {
        return obj;
    }
private:
    PyObject * obj;
};
