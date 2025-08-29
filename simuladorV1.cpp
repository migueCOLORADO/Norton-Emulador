using namespace std;
#include <bits/stdc++.h>


// ----------------------------- Utilidades de tiempo -----------------------------
using Clock = chrono::system_clock;
using TimePoint = chrono::time_point<Clock>;

static string hhmmss(TimePoint t) {
    time_t tt = Clock::to_time_t(t);
    tm local_tm{};
#if defined(_WIN32)
    localtime_s(&local_tm, &tt);
#else
    localtime_r(&tt, &local_tm);
#endif
    char buf[9];
    strftime(buf, sizeof(buf), "%H:%M:%S", &local_tm);
    return string(buf);
}

// ----------------------------- Datos y estructuras -----------------------------
enum class Risk { Alto, Bajo, Falsa };

static string riskToStr(Risk r) {
    switch (r) {
        case Risk::Alto:  return "Alto";
        case Risk::Bajo:  return "Bajo";
        case Risk::Falsa: return "Falsa Amenaza";
    }
    return "";
}

struct Mission {
    string id;
    string descripcion;
    Risk risk;
    TimePoint recibido;      // Hora de recepción (automática)
    TimePoint archivado;     // Hora en la que pasó a historial (para Falsa: = recibido)
    bool enHistorial = false;
};

struct SystemASG {
    // "Reloj virtual" para no depender del tiempo real
    TimePoint now;

    // Colas de pendientes (orden FIFO por llegada)
    deque<Mission> altas;
    deque<Mission> bajas;

    // Historial en el orden exacto en que se archivan
    vector<Mission> historial;

    // Tiempos de permanencia
    const chrono::seconds TTL_ALTO{60};   // 1 min
    const chrono::seconds TTL_BAJO{180};  // 3 min

    SystemASG() : now(Clock::now()) {}

    // Normaliza entrada de riesgo (acepta variantes comunes)
    static optional<Risk> parseRisk(string s) {
        // pasa a minúsculas y sin acentos/espacios claves
        auto lower = [](string x){
            for (auto &c : x) c = (char)tolower((unsigned char)c);
            return x;
        };
        s = lower(s);
        if (s == "alto") return Risk::Alto;
        if (s == "bajo") return Risk::Bajo;
        if (s == "falsa" || s == "falsaamenaza" || s == "falsa_amenaza" || s == "falsa-amenaza") return Risk::Falsa;
        return nullopt;
    }

    // Inserta en historial manteniendo orden por hora de archivado
    void pushHistorial(Mission m) {
        m.enHistorial = true;
        // Insertar preservando orden cronológico por 'archivado'
        auto it = std::upper_bound(historial.begin(), historial.end(), m.archivado,
            [](const TimePoint &tp, const Mission &mx){
                return tp < mx.archivado;
            });
        historial.insert(it, std::move(m));
    }

    // Limpia colas moviendo a historial las misiones expiradas al tiempo 't'
    void sweep(TimePoint t) {
        // Altas: expiración 60 s (archivado = recibido + 60s)
        while (!altas.empty()) {
            auto &m = altas.front();
            auto expiry = m.recibido + TTL_ALTO;
            if (expiry <= t) {
                Mission done = m;
                done.archivado = expiry;
                altas.pop_front();
                pushHistorial(std::move(done));
            } else break;
        }
        // Bajas: expiración 180 s (archivado = recibido + 180s)
        while (!bajas.empty()) {
            auto &m = bajas.front();
            auto expiry = m.recibido + TTL_BAJO;
            if (expiry <= t) {
                Mission done = m;
                done.archivado = expiry;
                bajas.pop_front();
                pushHistorial(std::move(done));
            } else break;
        }
    }

    // Agregar denuncia (hora se toma de 'now', no del usuario)
    void addMission(const string& id, Risk risk, const string& desc) {
        Mission m;
        m.id = id;
        m.descripcion = desc;
        m.risk = risk;
        m.recibido = now;

        if (risk == Risk::Falsa) {
            m.archivado = m.recibido; // se archiva de inmediato
            pushHistorial(std::move(m));
        } else if (risk == Risk::Alto) {
            altas.push_back(std::move(m));
        } else {
            bajas.push_back(std::move(m));
        }
    }

    // Avanza “tiempo virtual” N segundos (para pruebas)
    void waitSeconds(long long s) {
        if (s < 0) return;
        now += chrono::seconds(s);
        sweep(now);
    }

    // Imprime informe en el tiempo actual (previo sweep)
    void report(ostream& os) {
        sweep(now);

        os << "Lista de Amenazas Altas:\n";
        for (auto &m : altas) {
            os << m.id << ", " << hhmmss(m.recibido) << "\n";
        }
        if (altas.empty()) os << "(sin pendientes)\n";

        os << "Lista de Amenazas Bajas:\n";
        for (auto &m : bajas) {
            os << m.id << " (Bajo), " << hhmmss(m.recibido) << "\n";
        }
        if (bajas.empty()) os << "(sin pendientes)\n";

        os << "Historial:\n";
        if (historial.empty()) {
            os << "(vacío)\n";
        } else {
            for (auto &m : historial) {
                os << m.id << " (" << riskToStr(m.risk) << "), " << hhmmss(m.archivado) << "\n";
            }
        }
    }

    // Modo DEMO: reproduce exactamente el ejemplo del enunciado
    void demo(ostream& os) {
        // Para que los HH:MM:SS “calcen”, fijamos una base del reloj virtual a 10:42:50
        // (ajustando solamente la parte HH:MM:SS sobre la fecha actual).
        // Implementación simple: avanzamos hasta un segundo “cero” y desde allí simulamos.
        // Empezamos en now = Clock::now(); igual, usaremos WAIT para cuadrar segundos.
        // Secuencia del ejemplo:

        // t = 10:42:50
        // En la práctica, solo nos importa el orden y diferencia relativa entre eventos.
        // Reiniciemos estructuras para una DEMO limpia:
        altas.clear(); bajas.clear(); historial.clear();

        // Para forzar HH:MM:SS exactos, calculamos el offset al siguiente "10:42:50" del día actual.
        // Para simplificar, asumimos que la consola solo verá HH:MM:SS (la fecha no importa).
        // Construimos un tm “hoy a 10:42:50”:
        time_t tt = Clock::to_time_t(Clock::now());
        tm base{};
#if defined(_WIN32)
        localtime_s(&base, &tt);
#else
        localtime_r(&tt, &base);
#endif
        base.tm_hour = 10; base.tm_min = 42; base.tm_sec = 50;
        TimePoint start = Clock::from_time_t(mktime(&base));
        now = start;

        // M1 (Alto), 10:42:50
        addMission("M1", Risk::Alto, "");
        // 3s -> 10:42:53
        waitSeconds(3);
        // M2 (Falsa Amenaza), 10:42:53
        addMission("M2", Risk::Falsa, "");
        // 4s -> 10:42:57
        waitSeconds(4);
        // M3 (Alto), 10:42:57
        addMission("M3", Risk::Alto, "");
        // 14s -> 10:43:11
        waitSeconds(14);
        // M4 (Bajo)
        addMission("M4", Risk::Bajo, "");
        // 16s -> 10:43:27
        waitSeconds(16);
        // M5 (Falsa Amenaza)
        addMission("M5", Risk::Falsa, "");
        // 34s -> 10:44:01
        waitSeconds(34);
        // M6 (Bajo)
        addMission("M6", Risk::Bajo, "");
        // 36s -> 10:44:37
        waitSeconds(36);
        // M7 (Bajo)
        addMission("M7", Risk::Bajo, "");
        // 6s -> 10:44:43
        waitSeconds(6);
        // M8 (Alto)
        addMission("M8", Risk::Alto, "");

        // Reporte a las 10:45:00 (17s después de 10:44:43)
        waitSeconds(17);

        // Mostrar informe
        report(os);
    }
};

// ----------------------------- CLI simple -----------------------------
/*
Comandos soportados (entrada estándar):

  ADD <Id> <Riesgo> <Descripción libre...>
    - Riesgo: Alto | Bajo | Falsa (insensible a mayúsculas; admite "Falsa Amenaza")
    - La hora se toma automáticamente del reloj virtual.

  WAIT <segundos>
    - Avanza el reloj virtual N segundos (sin dormir realmente).
    - Esto permite probar expiraciones sin esperar en tiempo real.

  REPORT
    - Imprime el informe en el estado actual (tras barrer expiraciones).

  DEMO
    - Reproduce exactamente el ejemplo del enunciado y muestra el informe.

  EXIT
    - Termina el programa.

Ejemplo rápido manual:
  ADD M123 Alto Paquete sospechoso
  ADD M124 Falsa Amenaza Broma telefónica
  WAIT 65
  REPORT
*/
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    SystemASG sys;
    string line;

    // Si el programa se ejecuta sin interacción, puedes pegar aquí un "DEMO" automático:
    // sys.demo(cout); return 0;

    cout << "ASG listo. Escribe HELP para ver comandos.\n";
    while (true) {
        cout << "> ";
        if (!std::getline(cin, line)) break;
        if (line.empty()) continue;

        stringstream ss(line);
        string cmd; ss >> cmd;
        // Normalizar a mayúsculas
        for (auto &c : cmd) c = (char)toupper((unsigned char)c);

        if (cmd == "HELP") {
            cout << "Comandos:\n"
                 << "  ADD <Id> <Riesgo> <Descripcion...>\n"
                 << "  WAIT <segundos>\n"
                 << "  REPORT\n"
                 << "  DEMO\n"
                 << "  EXIT\n";
        } else if (cmd == "ADD") {
            string id, riesgoToken;
            if (!(ss >> id)) { cout << "Falta Id.\n"; continue; }
            if (!(ss >> riesgoToken)) { cout << "Falta Riesgo (Alto|Bajo|Falsa).\n"; continue; }

            // Resto de la línea es la descripción (opcional)
            string desc; getline(ss, desc);
            if (!desc.empty() && desc[0] == ' ') desc.erase(0,1);

            // Manejo especial por si usuario escribe "Falsa Amenaza" en dos palabras
            auto rParsed = SystemASG::parseRisk(riesgoToken);
            if (!rParsed.has_value()) {
                // Intentar leer una palabra más y ver si era "Falsa Amenaza"
                string maybe;
                string combined = riesgoToken;
                if (ss >> maybe) {
                    string combined2 = riesgoToken + " " + maybe;
                    auto r2 = SystemASG::parseRisk(combined2);
                    if (r2.has_value()) {
                        rParsed = r2;
                        // El resto de la línea tras esas dos palabras es la descripción
                        string rest;
                        getline(ss, rest);
                        if (!rest.empty() && rest[0] == ' ') rest.erase(0,1);
                        desc = rest;
                    } else {
                        // devolver el token extra a la descripción
                        if (!desc.empty()) desc = maybe + " " + desc; else desc = maybe;
                    }
                }
            }

            if (!rParsed.has_value()) {
                cout << "Riesgo invalido. Use: Alto | Bajo | Falsa Amenaza\n";
                continue;
            }

            sys.addMission(id, *rParsed, desc);
            cout << "Registrado " << id << " (" << riskToStr(*rParsed) << "), " << hhmmss(sys.now) << "\n";

        } else if (cmd == "WAIT") {
            long long s; 
            if (!(ss >> s)) { cout << "Uso: WAIT <segundos>\n"; continue; }
            sys.waitSeconds(s);
            cout << "Tiempo virtual: " << hhmmss(sys.now) << "\n";

        } else if (cmd == "REPORT") {
            sys.report(cout);

        } else if (cmd == "DEMO") {
            sys.demo(cout);

        } else if (cmd == "EXIT") {
            break;
        } else {
            cout << "Comando no reconocido. Escriba HELP.\n";
        }
    }
    return 0;
}