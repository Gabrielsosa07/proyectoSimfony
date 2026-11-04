import time
from validaciones import validar_cantidad, validar_nombre
from comercio import cursor, conexion


PRECIO_BASICO = 15
PRECIO_PREMIUM = 25
PRECIO_DLC = 5
PRECIO_PASE = 10

def pedir_pago(total):
    while True:
        try:
            pago = int(input("Abona con $: "))
            if pago >= total:
                return pago
            print(f"Error: El dinero abonado (${pago}) no alcanza para cubrir el total de ${total}.")
        except ValueError:
            print("Error: Debe ingresar un valor numérico.")

def guardar_venta(cliente, fecha, cant_b, cant_p, cant_dlc, cant_pase, total):
    linea = f"{cliente};{fecha};{cant_b};{cant_p};{cant_dlc};{cant_pase};{total}\n"
    try:
        cursor.execute("insert into ventas(cliente,fecha,cant_basico,cant_premium,cant_dlc,cant_pase,total)" 
        "values(?,?,?,?,?,?,?)",
        (cliente,fecha,cant_b,cant_p,cant_dlc,cant_pase,total))
    except Exception as e:
        print(f"Error al guardar venta: {e}")

def ingresar_pedido():
    print("\n" + "-" * 15 + " NUEVO PEDIDO " + "-" * 15)
    cliente = validar_nombre("Ingrese nombre del cliente: ")

    cant_b = validar_cantidad("Juego básico ($15)")
    cant_p = validar_cantidad("Juego premium ($25)")
    cant_dlc = validar_cantidad("DLC ($5)")
    cant_pase = validar_cantidad("Pase de temporada ($10)")

    total = (cant_b * PRECIO_BASICO +
             cant_p * PRECIO_PREMIUM +
             cant_dlc * PRECIO_DLC +
             cant_pase * PRECIO_PASE)

    if total == 0:
        print("No se seleccionó ningún producto. Pedido cancelado.")
        return 0

    print(f"Total ${total}")
    pago = pedir_pago(total)
    vuelto = pago - total
    print(f"Vuelto ${vuelto}")

    while True:
        confirma = input("¿Confirma pedido? Y/N: ").strip().upper()
        if confirma in ("Y", "N"):
            break
        print("Error: Ingrese 'Y' para confirmar o 'N' para cancelar.")

    if confirma == "Y":
        fecha = time.asctime()
        guardar_venta(cliente, fecha, cant_b, cant_p, cant_dlc, cant_pase, total)
        print("¡Pedido guardado con éxito!")
        return total
    else:
        print("Pedido cancelado. No se guardaron datos.")
        return 0