def trace1(file: object, lineno: object, name: object, pid: object, ppid: object, pr_name: object, dop: object = "") -> object:
    print(f"\t\t\t@#$%| 1 {file} {lineno}\t{name}\tpid={pid} \tparent pid={ppid}\t{pr_name} | {dop}")
    ...


def trace2(file: object, lineno: object, name: object, pid: object, ppid: object, pr_name: object, dop: object = "") -> object:
    print(f"\t\t\t@#$%| 2 {file} {lineno}\t{name}\tpid={pid} \tparent pid={ppid}\t{pr_name} | {dop}")

def trace_error(file: object, lineno: object, name: object, pid: object, ppid: object, pr_name: object, dop: object = "") -> object:
    print(f"\t\t\t@#$%| 2 {file} {lineno}\t{name}\tpid={pid} \tparent pid={ppid}\t{pr_name} | {dop}")
