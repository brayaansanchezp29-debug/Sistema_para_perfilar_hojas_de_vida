import json
import datetime
from typing import Dict, List, Optional

class SistemaHojasVida:
    def __init__(self):
        self.ofertas_laborales = []
        self.candidatos = []
        self.perfiles_laborales = []
    
    def registrar_oferta_laboral(self, titulo: str, empresa: str, descripcion: str, 
                               requisitos: List[str], salario: float = None):
        """Registra una nueva oferta laboral en la base de datos"""
        oferta = {
            'id': len(self.ofertas_laborales) + 1,
            'titulo': titulo,
            'empresa': empresa,
            'descripcion': descripcion,
            'requisitos': requisitos,
            'salario': salario,
            'fecha_publicacion': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'activa': True
        }
        self.ofertas_laborales.append(oferta)
        print(f" Oferta laboral '{titulo}' registrada exitosamente")
        return oferta['id']
    
    def registrar_candidato(self, nombre: str, email: str, telefono: str,
                          experiencia: List[Dict], educacion: List[Dict], 
                          habilidades: List[str], objetivo: str = ""):
        """Registra un nuevo candidato con su hoja de vida"""
        candidato = {
            'id': len(self.candidatos) + 1,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'experiencia': experiencia,
            'educacion': educacion,
            'habilidades': habilidades,
            'objetivo': objetivo,
            'fecha_registro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.candidatos.append(candidato)
        print(f" Candidato '{nombre}' registrado exitosamente")
        return candidato['id']
    
    def generar_perfil_laboral(self, candidato_id: int, oferta_id: int):
        """Genera un perfil laboral comparando candidato con oferta"""
        candidato = self.buscar_candidato(candidato_id)
        oferta = self.buscar_oferta(oferta_id)
        
        if not candidato or not oferta:
            print(" Candidato u oferta no encontrados")
            return None
        
        # Calcular compatibilidad
        compatibilidad = self._calcular_compatibilidad(candidato, oferta)
        
        perfil = {
            'id': len(self.perfiles_laborales) + 1,
            'candidato_id': candidato_id,
            'oferta_id': oferta_id,
            'compatibilidad': compatibilidad,
            'fecha_generacion': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'recomendaciones': self._generar_recomendaciones(candidato, oferta, compatibilidad)
        }
        
        self.perfiles_laborales.append(perfil)
        return perfil
    
    def _calcular_compatibilidad(self, candidato: Dict, oferta: Dict) -> Dict:
        """Calcula el porcentaje de compatibilidad entre candidato y oferta"""
        requisitos_oferta = [req.lower() for req in oferta['requisitos']]
        habilidades_candidato = [hab.lower() for hab in candidato['habilidades']]
        
        # Contar coincidencias de habilidades
        coincidencias = sum(1 for hab in habilidades_candidato if any(req in hab for req in requisitos_oferta))
        total_requisitos = len(requisitos_oferta)
        
        porcentaje_habilidades = (coincidencias / total_requisitos * 100) if total_requisitos > 0 else 0
        
        # Evaluar experiencia (simplificado)
        años_experiencia = sum(exp.get('años', 0) for exp in candidato['experiencia'])
        puntos_experiencia = min(años_experiencia * 10, 50)  # Máximo 50 puntos
        
        # Evaluar educación
        puntos_educacion = len(candidato['educacion']) * 15  # 15 puntos por título
        
        compatibilidad_total = min((porcentaje_habilidades + puntos_experiencia + puntos_educacion) / 2, 100)
        
        return {
            'total': round(compatibilidad_total, 2),
            'habilidades': round(porcentaje_habilidades, 2),
            'experiencia': puntos_experiencia,
            'educacion': puntos_educacion
        }
    
    def _generar_recomendaciones(self, candidato: Dict, oferta: Dict, compatibilidad: Dict) -> List[str]:
        """Genera recomendaciones para mejorar el perfil"""
        recomendaciones = []
        
        if compatibilidad['habilidades'] < 70:
            recomendaciones.append("Desarrollar habilidades específicas requeridas para el puesto")
        
        if compatibilidad['experiencia'] < 30:
            recomendaciones.append("Buscar experiencias adicionales en el campo laboral")
        
        if compatibilidad['total'] > 80:
            recomendaciones.append("¡Excelente candidato! Aplicar inmediatamente")
        elif compatibilidad['total'] > 60:
            recomendaciones.append("Buen candidato, considerar capacitación adicional")
        else:
            recomendaciones.append("Mejorar perfil antes de aplicar")
        
        return recomendaciones
    
    def buscar_candidato(self, candidato_id: int) -> Optional[Dict]:
        """Busca un candidato por ID"""
        return next((c for c in self.candidatos if c['id'] == candidato_id), None)
    
    def buscar_oferta(self, oferta_id: int) -> Optional[Dict]:
        """Busca una oferta por ID"""
        return next((o for o in self.ofertas_laborales if o['id'] == oferta_id), None)
    
    def mostrar_ofertas_activas(self):
        """Muestra todas las ofertas laborales activas"""
        print("\n OFERTAS LABORALES ACTIVAS:")
        print("-" * 50)
        for oferta in self.ofertas_laborales:
            if oferta['activa']:
                print(f"ID: {oferta['id']}")
                print(f"Título: {oferta['titulo']}")
                print(f"Empresa: {oferta['empresa']}")
                print(f"Requisitos: {', '.join(oferta['requisitos'])}")
                if oferta['salario']:
                    print(f"Salario: ${oferta['salario']:,.0f}")
                print("-" * 30)
    
    def mostrar_candidatos(self):
        """Muestra todos los candidatos registrados"""
        print("\n CANDIDATOS REGISTRADOS:")
        print("-" * 50)
        for candidato in self.candidatos:
            print(f"ID: {candidato['id']}")
            print(f"Nombre: {candidato['nombre']}")
            print(f"Email: {candidato['email']}")
            print(f"Habilidades: {', '.join(candidato['habilidades'])}")
            print(f"Experiencia: {len(candidato['experiencia'])} trabajos anteriores")
            print("-" * 30)
    
    def mostrar_perfil_detallado(self, perfil_id: int):
        """Muestra un perfil laboral detallado"""
        perfil = next((p for p in self.perfiles_laborales if p['id'] == perfil_id), None)
        if not perfil:
            print(" Perfil no encontrado")
            return
        
        candidato = self.buscar_candidato(perfil['candidato_id'])
        oferta = self.buscar_oferta(perfil['oferta_id'])
        
        print(f"\n PERFIL LABORAL #{perfil['id']}")
        print("=" * 60)
        print(f"Candidato: {candidato['nombre']}")
        print(f"Oferta: {oferta['titulo']} - {oferta['empresa']}")
        print(f"Compatibilidad Total: {perfil['compatibilidad']['total']}%")
        print(f"Habilidades: {perfil['compatibilidad']['habilidades']}%")
        print(f"Experiencia: {perfil['compatibilidad']['experiencia']} puntos")
        print(f"Educación: {perfil['compatibilidad']['educacion']} puntos")
        print("\n Recomendaciones:")
        for i, rec in enumerate(perfil['recomendaciones'], 1):
            print(f"  {i}. {rec}")
        print("=" * 60)


# Ejemplo de uso del sistema
def ejemplo_uso():
    sistema = SistemaHojasVida()
    
    print(" SISTEMA DE INFORMACIÓN - HOJAS DE VIDA")
    print("=" * 50)
    
    # Registrar ofertas laborales
    print("\n1️ REGISTRANDO OFERTAS LABORALES:")
    sistema.registrar_oferta_laboral(
        titulo="Desarrollador Python",
        empresa="TechCorp",
        descripcion="Desarrollador backend con experiencia en Python y Django",
        requisitos=["Python", "Django", "PostgreSQL", "Git"],
        salario=4500000
    )
    
    sistema.registrar_oferta_laboral(
        titulo="Analista de Datos",
        empresa="DataCorp",
        descripcion="Analista para procesamiento y visualización de datos",
        requisitos=["Python", "Pandas", "SQL", "Tableau"],
        salario=3800000
    )
    
    # Registrar candidatos
    print("\n2️ REGISTRANDO CANDIDATOS:")
    sistema.registrar_candidato(
        nombre="Ana García",
        email="ana.garcia@email.com",
        telefono="555-0123",
        experiencia=[
            {"empresa": "StartupXYZ", "cargo": "Junior Developer", "años": 2},
            {"empresa": "WebSolutions", "cargo": "Python Developer", "años": 1}
        ],
        educacion=[
            {"titulo": "Ingeniería de Sistemas", "institucion": "Universidad Nacional"},
            {"titulo": "Curso Django", "institucion": "Platzi"}
        ],
        habilidades=["Python", "Django", "HTML", "CSS", "JavaScript", "Git"],
        objetivo="Desarrollar aplicaciones web escalables"
    )
    
    sistema.registrar_candidato(
        nombre="Carlos Ruiz",
        email="carlos.ruiz@email.com",
        telefono="555-0456",
        experiencia=[
            {"empresa": "Analytics Inc", "cargo": "Data Analyst", "años": 3}
        ],
        educacion=[
            {"titulo": "Estadística", "institucion": "Universidad Javeriana"}
        ],
        habilidades=["Python", "Pandas", "SQL", "Excel", "R"],
        objetivo="Especializar en ciencia de datos"
    )
    
    # Mostrar datos registrados
    sistema.mostrar_ofertas_activas()
    sistema.mostrar_candidatos()
    
    # Generar perfiles laborales
    print("\n3️ GENERANDO PERFILES LABORALES:")
    perfil1 = sistema.generar_perfil_laboral(candidato_id=1, oferta_id=1)
    perfil2 = sistema.generar_perfil_laboral(candidato_id=2, oferta_id=2)
    
    # Mostrar perfiles detallados
    sistema.mostrar_perfil_detallado(1)
    sistema.mostrar_perfil_detallado(2)


# Ejecutar ejemplo
if __name__ == "__main__":
    ejemplo_uso()