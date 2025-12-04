import os
from modules.search_module import (
    get_suid_bit, get_sgid_bit, get_word_writable_files, 
    get_word_writable_dirs, get_cron_jobs, get_root_process
)
from knowlege_base.vulnerability_db import VULNERABILITY_DATABASE, VULNERABLE_BINARIES

class PrivilegeEscalationAnalyzer:
    def __init__(self):
        self.findings = []
    
    def analyze_suid_binaries(self):
        """Анализ SUID бинарников"""
        print("\n[*] Анализирую SUID бинарники...")
        suid_files = get_suid_bit()
        
        for binary_path in suid_files:
            binary_name = os.path.basename(binary_path)
            
            # Проверяем, известна ли уязвимость
            vuln_info = VULNERABLE_BINARIES.get(binary_name)
            
            finding = {
                "type": "SUID_BINARY",
                "path": binary_path,
                "name": binary_name,
                "risk_level": "HIGH",
                "description": f"SUID бинарник: {binary_name}",
                "details": vuln_info
            }
            
            if vuln_info:
                finding["risk_level"] = "CRITICAL"
                finding["description"] = f"⚠️ ИЗВЕСТНЫЙ уязвимый SUID: {binary_name} - {', '.join(vuln_info['known_issues'])}"
            
            self.findings.append(finding)
        
        return len(suid_files)
    
    def analyze_sgid_binaries(self):
        """Анализ SGID бинарников"""
        print("\n[*] Анализирую SGID бинарники...")
        sgid_files = get_sgid_bit()
        
        for binary_path in sgid_files:
            binary_name = os.path.basename(binary_path)
            
            vuln_info = VULNERABLE_BINARIES.get(binary_name)
            
            finding = {
                "type": "SGID_BINARY",
                "path": binary_path,
                "name": binary_name,
                "risk_level": "MEDIUM",
                "description": f"SGID бинарник: {binary_name}",
                "details": vuln_info
            }
            
            if vuln_info:
                finding["risk_level"] = "HIGH"
            
            self.findings.append(finding)
        
        return len(sgid_files)
    
    def analyze_world_writable(self):
        """Анализ world-writable файлов и директорий"""
        print("\n[*] Анализирую world-writable файлы...")
        
        ww_files = get_word_writable_files()
        for file_path in ww_files:
            finding = {
                "type": "WORLD_WRITABLE_FILE",
                "path": file_path,
                "risk_level": "CRITICAL",
                "description": f"⚠️ КРИТИЧНО: World-writable файл: {file_path}",
                "impact": "Может быть изменен любым пользователем"
            }
            self.findings.append(finding)
        
        print("[*] Анализирую world-writable директории...")
        ww_dirs = get_word_writable_dirs()
        for dir_path in ww_dirs:
            finding = {
                "type": "WORLD_WRITABLE_DIR",
                "path": dir_path,
                "risk_level": "CRITICAL",
                "description": f"⚠️ КРИТИЧНО: World-writable директория: {dir_path}",
                "impact": "Туда можно создать вредоносные файлы"
            }
            self.findings.append(finding)
        
        return len(ww_files) + len(ww_dirs)
    
    def analyze_cron_jobs(self):
        """Анализ cron задач"""
        print("\n[*] Анализирую cron задачи...")
        crons = get_cron_jobs()
        
        for cron_entry in crons:
            # Простой анализ: ищем скрипты, запускаемые от root
            if 'root' in cron_entry or '/root' in cron_entry:
                finding = {
                    "type": "CRON_JOB",
                    "path": cron_entry,
                    "risk_level": "HIGH",
                    "description": f"Cron задача от root: {cron_entry[:80]}...",
                    "impact": "Если скрипт world-writable, возможно повышение привилегий"
                }
                self.findings.append(finding)
        
        return len(crons)
    
    def generate_report(self):
        """Генерация отчета с рекомендациями"""
        print("\n" + "="*80)
        print("ОТЧЕТ: АНАЛИЗ УЯЗВИМОСТЕЙ ДЛЯ ПОВЫШЕНИЯ ПРИВИЛЕГИЙ В LINUX")
        print("="*80)
        
        if not self.findings:
            print("\n✓ Никаких подозрительных нахождений не обнаружено")
            return
        
        # Сортируем по уровню риска
        risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_findings = sorted(
            self.findings, 
            key=lambda x: risk_order.get(x.get("risk_level"), 4)
        )
        
        # Группируем по типу
        by_type = {}
        for finding in sorted_findings:
            ftype = finding["type"]
            if ftype not in by_type:
                by_type[ftype] = []
            by_type[ftype].append(finding)
        
        # Выводим по категориям
        for ftype, findings_list in by_type.items():
            print(f"\n{'─'*80}")
            print(f"[{ftype}] - {len(findings_list)} находок")
            print(f"{'─'*80}")
            
            for i, finding in enumerate(findings_list[:5], 1):  # Показываем первые 5
                print(f"\n  {i}. {finding['description']}")
                print(f"     Risk Level: {finding['risk_level']}")
                if "impact" in finding:
                    print(f"     Impact: {finding['impact']}")
                if "details" in finding and finding["details"]:
                    print(f"     Details: {finding['details']}")
        
        print(f"\n{'='*80}")
        print(f"ИТОГО: Найдено {len(self.findings)} потенциальных векторов повышения привилегий")
        print(f"  - CRITICAL: {sum(1 for f in self.findings if f['risk_level'] == 'CRITICAL')}")
        print(f"  - HIGH: {sum(1 for f in self.findings if f['risk_level'] == 'HIGH')}")
        print(f"  - MEDIUM: {sum(1 for f in self.findings if f['risk_level'] == 'MEDIUM')}")
        print(f"{'='*80}\n")
    
    def run_full_analysis(self):
        """Запустить полный анализ"""
        print("\n[+] Запускаю полный анализ системы на уязвимости...")
        
        count = 0
        count += self.analyze_suid_binaries()
        count += self.analyze_sgid_binaries()
        count += self.analyze_world_writable()
        count += self.analyze_cron_jobs()
        
        print(f"\n[+] Всего проверено объектов: {count}")
        
        self.generate_report()

if __name__ == "__main__":
    analyzer = PrivilegeEscalationAnalyzer()
    analyzer.run_full_analysis()
