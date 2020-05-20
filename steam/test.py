s = """Machine
NumberOfSections
TimeDateStamp
PointerToSymbolTable
NumberOfSymbols
SizeOfOptionalHeader
Characteristics"""
s = s.strip()
s = s.replace(",", " ")
s = s.replace(";", " ")

s = s.split("\n")
i = 0
N = len(s)

init_statement = """
QVector<int> it_size;
it_size.reserve(10);
QVector<int> it_value;
it_size.reserve(10);
"""
print(init_statement)
for it in s:
    a = ("auto it%d = p->%s;") % (i, it.strip())
    i = i + 1
    print(a)

# 7 is 0..6
for i in range(N):
    a = ("it_value.push_back(it%d);") % (i)
    print(a)

# 7 is 0..6
for i in range(N):
    a = ("it_size.push_back(sizeof(it%d));") % (i)
    print(a)

va_init = """
// VA初始化
for (auto item : it_size) {
    d.va.append(QString("%1").arg(startVa, 8, 16, QChar('0')).toUpper());
    startVa += item;
}
// 初始化data
for (int i = 0; i < it_value.size(); ++i) {
    d.data.push_back(QString("%1").arg(it_value[i], it_size[i] << 1, 16, QChar('0')).toUpper());
}
"""
print(va_init)

# desc 初始化
desc = '//初始化desc\nQString desc = "'
for it in s:
    desc += it
    desc += ","
desc = desc.rstrip(",")

desc += '";\n'
desc += 'd.desc = desc.split(",");'
print(desc)
