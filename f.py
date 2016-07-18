import check

a = (
    "bok/obsed/201511/files.J7330.lst",
    "bok/obsed/201511/files.J7332.lst",
    "bok/obsed/201511/files.J7333.lst",
    "bok/obsed/201511/files.J7334.lst",
    "bok/obsed/201511/files.J7335.lst",
    "bok/obsed/201511/files.J7336.lst",
    "bok/obsed/201511/files.J7337.lst",
    "bok/obsed/201512/files.J7360.lst",
    "bok/obsed/201512/files.J7361.lst",
    "bok/obsed/201512/files.J7362.lst",
    "bok/obsed/201512/files.J7363.lst",
    "bok/obsed/201512/files.J7364.lst",
    "bok/obsed/201512/files.J7365.lst",
    "bok/obsed/201512/files.J7366.lst",
    "bok/obsed/201512/files.J7367.lst",
    "bok/obsed/201512/files.J7370.lst",
    "bok/obsed/201512/files.J7371.lst",
    "bok/obsed/201512/files.J7372.lst",
    "bok/obsed/201512/files.J7373.lst",
    "bok/obsed/201601/files.J7418.lst",
    "bok/obsed/201601/files.J7419.lst",
    "bok/obsed/201601/files.J7420.lst",
    "bok/obsed/201602/files.J7448.lst",
    "bok/obsed/201602/files.J7449.lst",
    "bok/obsed/201602/files.J7450.lst",
    "bok/obsed/201603A/files.J7462.lst",
    "bok/obsed/201603A/files.J7463.lst",
    "bok/obsed/201603A/files.J7464.lst",
    "bok/obsed/201603B/files.J7477.lst",
    "bok/obsed/201603B/files.J7478.lst",
    "bok/obsed/201603B/files.J7479.lst" )

for f in a :
    f2 = f[0:-15] + "check" + f[-10:]
    print f, f2
    check.check(f, f2)
