#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test del endpoint validar_imagen con validación SRI en prioritarias corregido
"""

import requests
import json
import os
import base64

def test_endpoint_prioritarias_corregido():
    """Test del endpoint validar_imagen con SRI en prioritarias corregido"""
    print("🔬 TEST ENDPOINT CON SRI EN PRIORITARIAS CORREGIDO")
    print("=" * 70)
    
    # URL del endpoint
    url = "http://localhost:8000/validar-imagen"
    
    # Imagen de prueba
    img_path = "helpers/IMG/Captura de pantalla 2025-09-19 120741.png"
    
    if not os.path.exists(img_path):
        print(f"❌ No se encontró la imagen: {img_path}")
        return
    
    print(f"📸 Procesando imagen: {img_path}")
    
    # Leer imagen y convertir a base64
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    # Datos de la petición
    data = {
        "imagen_base64": img_base64
    }
    
    try:
        # Hacer petición
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Respuesta exitosa!")
            
            # Verificar sri_verificado principal
            sri_verificado_principal = result.get('sri_verificado', False)
            mensaje_principal = result.get('mensaje', 'N/A')
            
            print(f"\n🔑 VALIDACIÓN SRI PRINCIPAL:")
            print(f"   sri_verificado: {sri_verificado_principal}")
            print(f"   mensaje: {mensaje_principal}")
            
            # Verificar riesgo y prioritarias
            if 'riesgo' in result:
                riesgo = result['riesgo']
                print(f"\n⚠️  ANÁLISIS DE RIESGO:")
                print(f"   Score: {riesgo.get('score', 'N/A')}")
                print(f"   Nivel: {riesgo.get('nivel', 'N/A')}")
                print(f"   Es falso probable: {riesgo.get('es_falso_probable', 'N/A')}")
                
                # Verificar prioritarias
                prioritarias = riesgo.get('prioritarias', [])
                print(f"\n🔍 PRIORITARIAS ({len(prioritarias)}):")
                
                for i, check in enumerate(prioritarias):
                    print(f"   {i+1}. {check.get('check', 'N/A')} (penalización: {check.get('penalizacion', 0)})")
                    
                    # Mostrar detalles de validación SRI
                    if check.get('check') == "Validación SRI":
                        detalle = check.get('detalle', {})
                        print(f"      SRI Verificado: {detalle.get('sri_verificado', 'N/A')}")
                        print(f"      Clave Acceso: {detalle.get('clave_acceso', 'N/A')[:20]}...")
                        print(f"      Estado SRI: {detalle.get('estado_sri', 'N/A')}")
                        print(f"      RUC Emisor: {detalle.get('ruc_emisor', 'N/A')}")
                        print(f"      Tipo: {detalle.get('tipo_comprobante', 'N/A')}")
                        print(f"      Serie: {detalle.get('serie', 'N/A')}")
                        print(f"      Secuencial: {detalle.get('secuencial', 'N/A')}")
                        print(f"      Interpretación: {detalle.get('interpretacion', 'N/A')}")
                        print(f"      Recomendación: {detalle.get('recomendacion', 'N/A')}")
                        
                        # Verificar que los valores son correctos
                        if detalle.get('sri_verificado') == True and detalle.get('estado_sri') == "AUTORIZADO":
                            print("      ✅ VALIDACIÓN SRI CORRECTA EN PRIORITARIAS!")
                        else:
                            print("      ❌ VALIDACIÓN SRI INCORRECTA EN PRIORITARIAS!")
                
                # Verificar secundarias
                secundarias = riesgo.get('secundarias', [])
                print(f"\n🔍 SECUNDARIAS ({len(secundarias)}):")
                for i, check in enumerate(secundarias):
                    print(f"   {i+1}. {check.get('check', 'N/A')} (penalización: {check.get('penalizacion', 0)})")
                
                # Verificar adicionales
                adicionales = riesgo.get('adicionales', [])
                print(f"\n🔍 ADICIONALES ({len(adicionales)}):")
                for i, check in enumerate(adicionales):
                    print(f"   {i+1}. {check.get('check', 'N/A')} (penalización: {check.get('penalizacion', 0)})")
            
            # Verificar factura
            if 'factura' in result:
                factura = result['factura']
                print(f"\n📄 FACTURA:")
                print(f"   RUC: {factura.get('ruc', 'N/A')}")
                print(f"   Clave Acceso: {factura.get('claveAcceso', 'N/A')}")
                print(f"   SRI Verificado: {factura.get('sri_verificado', 'N/A')}")
                
                if 'validacion_sri' in factura:
                    validacion = factura['validacion_sri']
                    print(f"   Validación SRI: {validacion.get('valido', 'N/A')}")
                    print(f"   Estado: {validacion.get('consulta_sri', {}).get('estado', 'N/A')}")
            
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está ejecutándose el servidor?")
        print("Ejecuta: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_endpoint_prioritarias_corregido()
