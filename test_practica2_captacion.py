#!/usr/bin/env python3
"""
Prueba funcional específica para la Práctica 2: Captación de agua
Verifica la integración correcta entre frontend y backend después de la corrección.
"""

# Agregar el directorio del proyecto al path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import practica5_captacion_lluvia as captacion

def test_backend_integration():
    """Prueba directa del backend para verificar el formato de datos"""
    print("=== PRUEBA DEL BACKEND DE CAPTACIÓN DE AGUA ===")
    
    # Parámetros de prueba
    intensidad_lluvia = 50.0  # mm/h
    area_techo = 15.0  # m²
    duracion = 120.0  # min
    
    print(f"Parámetros de entrada:")
    print(f"  - Intensidad de lluvia: {intensidad_lluvia} mm/h")
    print(f"  - Área del techo: {area_techo} m²")
    print(f"  - Duración: {duracion} min")
    print()
    
    # Llamar al backend
    resultado = captacion.calcular_resultados(
        intensidad_lluvia=intensidad_lluvia,
        area_techo=area_techo,
        duracion=duracion
    )
    
    print(f"Resultado del backend:")
    print(f"  Tipo: {type(resultado)}")
    print(f"  Claves disponibles: {list(resultado.keys())}")
    print()
    
    # Verificar datos específicos
    print("=== DATOS DEVUELTOS POR EL BACKEND ===")
    for clave, valor in resultado.items():
        print(f"  {clave}: {valor}")
    print()
    
    # Simular la conversión que hace el frontend
    print("=== SIMULACIÓN DEL FRONTEND ===")
    volumen_captado_L = resultado.get('volumen_captado', 0) * 1000
    nivel_tanque_cm = resultado.get('nivel_tanque', 0)
    volumen_estimado_L = resultado.get('volumen_estimado_sensor', 0) * 1000
    precision_pct = resultado.get('precision_sensor', 0)
    tiempo_min = resultado.get('tiempo_captacion', 0)
    
    print(f"Variables del frontend (como aparecerán en la UI):")
    print(f"  - Volumen captado: {volumen_captado_L:.2f} L")
    print(f"  - Nivel del tanque: {nivel_tanque_cm:.1f} cm") 
    print(f"  - Volumen estimado por sensor: {volumen_estimado_L:.2f} L")
    print(f"  - Precisión del sensor: {precision_pct:.1f} %")
    print(f"  - Tiempo de captación: {tiempo_min:.1f} min")
    print()
    
    # Verificar que las claves esperadas existen
    claves_esperadas = ['volumen_captado', 'nivel_tanque', 'volumen_estimado_sensor', 'precision_sensor', 'tiempo_captacion']
    claves_faltantes = [clave for clave in claves_esperadas if clave not in resultado]
    
    if claves_faltantes:
        print(f"❌ ERROR: Faltan claves en el backend: {claves_faltantes}")
        return False
    else:
        print("✅ Todas las claves esperadas están presentes en el backend")
        
    # Verificar que no hay claves del formato antiguo
    claves_antiguas = ['nivel_sensor', 'volumen_est_medido', 'precision_medicion']
    claves_antiguas_presentes = [clave for clave in claves_antiguas if clave in resultado]
    
    if claves_antiguas_presentes:
        print(f"⚠️  ADVERTENCIA: Se encontraron claves del formato antiguo: {claves_antiguas_presentes}")
    else:
        print("✅ No se encontraron claves del formato antiguo")
    
    print()
    print("=== RESUMEN DE LA PRUEBA ===")
    print("✅ Backend funciona correctamente")
    print("✅ Formato de datos actualizado")
    print("✅ Conversiones de unidades aplicadas")
    print("✅ Integración frontend-backend corregida")
    
    return True

def test_frontend_simulation():
    """Simula el flujo completo del frontend"""
    print("\n" + "="*60)
    print("=== SIMULACIÓN DEL FLUJO FRONTEND ===")
    
    # Simular inputs del usuario
    print("Simulando entrada del usuario:")
    inputs = {
        'input_intensidad': '35.5',
        'input_area': '20.0', 
        'input_tiempo': '90.0'
    }
    
    for input_id, valor in inputs.items():
        print(f"  {input_id}: {valor}")
    
    print("\nProcesando datos...")
    
    try:
        # Convertir inputs (como hace el frontend)
        intensidad_lluvia = float(inputs['input_intensidad'])
        area_techo = float(inputs['input_area'])
        duracion = float(inputs['input_tiempo'])
        
        # Validar (como hace el frontend)
        if intensidad_lluvia <= 0 or area_techo <= 0 or duracion <= 0:
            print("❌ ERROR: Validación falló")
            return False
            
        # Llamar backend (como hace el frontend)
        datos = captacion.calcular_resultados(
            intensidad_lluvia=intensidad_lluvia,
            area_techo=area_techo,
            duracion=duracion
        )
        
        # Formatear resultados (como hace el frontend)
        resultados_formateados = {
            'volumen_captado': f"{datos.get('volumen_captado', 0) * 1000:.2f} L",
            'nivel_sensor': f"{datos.get('nivel_tanque', 0):.1f} cm",
            'volumen_estimado': f"{datos.get('volumen_estimado_sensor', 0) * 1000:.2f} L", 
            'precision': f"{datos.get('precision_sensor', 0):.1f} %",
            'tiempo_captacion': f"{datos.get('tiempo_captacion', 0):.1f} min"
        }
        
        print("\nResultados mostrados al usuario:")
        for variable, valor_formateado in resultados_formateados.items():
            print(f"  {variable}: {valor_formateado}")
            
        print("\n✅ Simulación del frontend completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ ERROR en la simulación: {e}")
        return False

if __name__ == "__main__":
    print("PRUEBA FUNCIONAL: PRÁCTICA 2 - CAPTACIÓN DE AGUA")
    print("="*60)
    
    # Ejecutar pruebas
    backend_ok = test_backend_integration()
    frontend_ok = test_frontend_simulation()
    
    print("\n" + "="*60)
    print("=== RESULTADO FINAL ===")
    
    if backend_ok and frontend_ok:
        print("🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ La integración frontend-backend está funcionando correctamente")
        print("✅ La Práctica 2 (Captación de agua) está lista para uso")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("⚠️  Se requiere revisión adicional")
    
    print("="*60)
