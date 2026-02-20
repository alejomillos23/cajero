from datetime import datetime

print("CAJERO AUTOMÁTICO")

saldo = 0
#ejemplo

while True:
    print("\nSeleccione una opción:")
    print("1. Consultar saldo")
    print("2. Depositar dinero")
    print("3. Retirar dinero")
    print("4. Salir")

    opcion = input("Ingrese una opción: ").strip()

    if opcion == "":
        print("Debe ingresar una opción")
        continue

    if opcion == "1":
        print("Su saldo actual es:", saldo)

    elif opcion == "2":
        try:
            monto = input("Ingrese el monto a depositar: ").strip()
            monto = monto.replace(",", ".")
            deposito = float(monto)

            if deposito <= 0:
                print("El monto debe ser mayor a cero")
            elif deposito > 10000000:
                print("Monto demasiado grande")
            else:
                saldo += deposito

                ahora = datetime.now()
                fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")

                print(f"{fecha_hora} | Depósito realizado: ${deposito}")
                print("Nuevo saldo:", saldo)

        except:
            print("Error: debe ingresar un número válido")

    elif opcion == "3":
        if saldo == 0:
            print("No tiene saldo disponible para retirar")
        else:
            try:
                monto = input("Ingrese el monto a retirar: ").strip()
                monto = monto.replace(",", ".")
                retiro = float(monto)

                if retiro <= 0:
                    print("El monto debe ser mayor a cero")
                elif retiro > saldo:
                    print("Fondos insuficientes")
                else:
                    saldo -= retiro

                    ahora = datetime.now()
                    fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")

                    print(f"{fecha_hora} | Retiro realizado: ${retiro}")
                    print("Nuevo saldo:", saldo)

            except:
                print("Error: debe ingresar un número válido")


    elif opcion == "4":
        ahora = datetime.now()
        fecha_hora = ahora.strftime("%d/%m/%Y %H:%M:%S")

        print("Gracias por usar el cajero automático")
        print("Fecha y hora de salida:", fecha_hora)
        break

    else:
        print("Opción no válida, intente de nuevo")