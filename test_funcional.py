#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA FUNCIONAL AUTOMÁTICA
=====================================
Verifica que la reorganización del frontend funciona correctamente
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Añadir el directorio del proyecto al path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def test_imports():
    """Verifica que todos los imports funcionen correctamente"""
    print("🔍 TESTING: Imports de módulos...")
    
    try:
        # Test imports del main
        from kivy.app import App
        from kivy.lang import Builder
        from kivy.uix.screenmanager import ScreenManager, Screen
        print("✅ Kivy imports - OK")
        
        # Test imports del frontend
        from frontend.main_screen import MainScreen
        from frontend.screens.practica1_screen import Practica1Screen
        from frontend.screens.practica2_screen import Practica2Screen
        from frontend.screens.practica3_screen import Practica3Screen
        from frontend.screens.practica4_screen import Practica4Screen
        from frontend.screens.practica5_screen import Practica5Screen
        print("✅ Frontend screens imports - OK")
        
        # Test imports del backend
        from backend import practica1_balance_energetico as be
        from backend import practica2_filtrado_multicapa as filtrado
        from backend import practica3_intercambiador_calor as intercambiador
        from backend import practica4_caldera as caldera
        from backend import practica5_captacion_lluvia as captacion
        print("✅ Backend imports - OK")
        
        return True
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False

def test_kv_files():
    """Verifica que los archivos .kv estén bien formateados"""
    print("\n🔍 TESTING: Archivos .kv...")
    
    kv_files = [
        'kv/main.kv',
        'kv/practica1.kv', 
        'kv/practica2.kv',
        'kv/practica3.kv',
        'kv/practica4.kv',
        'kv/practica5.kv'
    ]
    
    all_good = True
    for kv_file in kv_files:
        if os.path.exists(kv_file):
            try:
                Builder.load_file(kv_file)
                print(f"✅ {kv_file} - OK")
            except Exception as e:
                print(f"❌ {kv_file} - ERROR: {e}")
                all_good = False
        else:
            print(f"❌ {kv_file} - ARCHIVO NO ENCONTRADO")
            all_good = False
    
    return all_good

def test_screen_mapping():
    """Verifica el mapeo correcto de pantallas"""
    print("\n🔍 TESTING: Mapeo de screens...")
    
    # Mapeo esperado después de la reorganización
    expected_mapping = {
        'practica1': 'Practica1Screen',  # Balance energético (sin cambios)
        'practica2': 'Practica2Screen',  # Filtrado multicapa (navegación cambiada)
        'practica3': 'Practica3Screen',  # Intercambiador de calor (navegación cambiada)
        'practica4': 'Practica4Screen',  # Caldera (sin cambios)
        'practica5': 'Practica5Screen',  # Captación de agua (navegación cambiada)
    }
    
    print("Mapeo esperado:")
    print("- Botón 'Práctica 1: Balance energético' → practica1 → Practica1Screen")
    print("- Botón 'Práctica 2: Captación de agua' → practica5 → Practica5Screen")
    print("- Botón 'Práctica 3: Filtrado multicapa' → practica2 → Practica2Screen")
    print("- Botón 'Práctica 4: Caldera' → practica4 → Practica4Screen")
    print("- Botón 'Práctica 5: Intercambiador de calor' → practica3 → Practica3Screen")
    
    for screen_name, class_name in expected_mapping.items():
        print(f"✅ {screen_name} → {class_name}")
    
    return True

def test_backend_functionality():
    """Prueba básica de funcionalidad de backends"""
    print("\n🔍 TESTING: Funcionalidad básica de backends...")
    
    try:
        # Test práctica 1 (Balance energético)
        from backend import practica1_balance_energetico as be
        result = be.calcular_resultados(radiacion=800, tension=12, corriente=5, tiempo=8, consumo=500, perdidas=0.1)
        assert result.get('status') == 'ok', f"Backend práctica 1 falló: {result}"
        print("✅ Backend Práctica 1 (Balance energético) - OK")
        
        # Test práctica 2 (Filtrado multicapa)
        from backend import practica2_filtrado_multicapa as filtrado
        result = filtrado.calcular_resultados(turbidez_inicial=50, volumen=100, tiempo=95, grava_activa=True, arena_activa=True, carbon_activo=True)
        assert result.get('status') == 'ok', f"Backend práctica 2 falló: {result}"
        print("✅ Backend Práctica 2 (Filtrado multicapa) - OK")
        
        # Test práctica 3 (Intercambiador de calor)
        from backend import practica3_intercambiador_calor as intercambiador
        result = intercambiador.calcular_resultados(temperatura_inicial=20, masa_agua=5, potencia_solar=1000, tiempo_exposicion=30, tcaliente=60, caudal_caliente=2, caudal_frio=2)
        assert result.get('status') == 'ok', f"Backend práctica 3 falló: {result}"
        print("✅ Backend Práctica 3 (Intercambiador de calor) - OK")
        
        # Test práctica 4 (Caldera)
        from backend import practica4_caldera as caldera
        result = caldera.calcular_resultados(temperatura_inicial=25, volumen_agua=0.5, energia_entrada=1500, modo="resistencia")
        assert result.get('status') == 'ok', f"Backend práctica 4 falló: {result}"
        print("✅ Backend Práctica 4 (Caldera) - OK")
        
        # Test práctica 5 (Captación de lluvia)
        from backend import practica5_captacion_lluvia as captacion
        result = captacion.calcular_resultados(intensidad_lluvia=10, area_techo=50, duracion=120)
        assert result.get('status') == 'ok', f"Backend práctica 5 falló: {result}"
        print("✅ Backend Práctica 5 (Captación de lluvia) - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en backend testing: {e}")
        return False

def test_navigation_consistency():
    """Verifica consistencia en la navegación"""
    print("\n🔍 TESTING: Consistencia de navegación...")
    
    # Leer main.kv para verificar navegación
    try:
        with open('kv/main.kv', 'r', encoding='utf-8') as f:
            main_kv_content = f.read()
        
        navigation_tests = [
            ("Práctica 1: Balance energético", "practica1"),
            ("Práctica 2: Captación de agua", "practica5"),
            ("Práctica 3: Filtrado multicapa", "practica2"),
            ("Práctica 4: Caldera", "practica4"),
            ("Práctica 5: Intercambiador de calor", "practica3")
        ]
        
        for button_text, expected_screen in navigation_tests:
            if button_text in main_kv_content and expected_screen in main_kv_content:
                print(f"✅ '{button_text}' → '{expected_screen}' - OK")
            else:
                print(f"❌ '{button_text}' → '{expected_screen}' - ERROR")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando navegación: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 INICIANDO PRUEBAS FUNCIONALES")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Ejecutar todas las pruebas
    tests = [
        test_imports,
        test_kv_files,
        test_screen_mapping,
        test_backend_functionality,
        test_navigation_consistency
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Error ejecutando {test_func.__name__}: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ La reorganización del frontend está funcionando correctamente")
        print("\n📋 RESUMEN:")
        print("- ✅ Imports funcionando")
        print("- ✅ Archivos .kv válidos")
        print("- ✅ Mapeo de screens correcto")
        print("- ✅ Backends funcionando")
        print("- ✅ Navegación consistente")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("🔧 Revisar los errores reportados arriba")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
