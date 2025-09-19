import cv2, dlib, numpy as np, pickle, os, time

PREDICTOR = "shape_predictor_5_face_landmarks.dat"
RECOG = "dlib_face_recognition_resnet_model_v1.dat"
DB_FILE = "db.pkl"
THRESH = 0.6
BAUD = 9600

db = pickle.load(open(DB_FILE,"rb")) if os.path.exists(DB_FILE) else {}
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR)
rec = dlib.face_recognition_model_v1(RECOG)

cap = cv2.VideoCapture(0)
validando = False
ultimo = 0
cooldown = 3

print("[E]=Cadastrar  [V]=Validar ON/OFF  [Q]=Sair")

while True:
    ok, frame = cap.read()
    if not ok: break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rects = detector(rgb, 1)

    for r in rects:
        shape = sp(rgb, r)
        chip = dlib.get_face_chip(rgb, shape)
        vec = np.array(rec.compute_face_descriptor(chip), dtype=np.float32)

        if validando and db:
            nome, dist, tipo = "Desconhecido", 999, None
            for n, (v, t) in db.items():
                d = np.linalg.norm(vec - v)
                if d < dist:
                    nome, dist, tipo = n, d, t
            if dist > THRESH:
                nome, tipo = "Desconhecido", None

            # Defina as cores por tipo
            if nome == "Desconhecido":
                color = (0, 0, 255)  # Vermelho
            elif tipo == "acessor":
                color = (255, 255, 0)  # Amarelo
            elif tipo == "investidor":
                color = (0, 255, 255)  # Ciano
            else:
                color = (0, 255, 0)  # Verde padrão

            cv2.rectangle(frame, (r.left(), r.top()), (r.right(), r.bottom()), color, 2)
            cv2.putText(frame, f"{nome} ({tipo if tipo else ''})", (r.left(), r.top()-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Faces", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): break
    if k == ord('v'): validando = not validando
    if k == ord('e') and len(rects) == 1:
        nome = input("Nome: ").strip()
        if nome:
            tipo = input("Tipo (acessor/investidor): ").strip().lower()
            if tipo not in ["acessor", "investidor"]:
                print("Tipo inválido! Use 'acessor' ou 'investidor'.")
            else:
                db[nome] = (vec, tipo)
                pickle.dump(db, open(DB_FILE,"wb"))
                print(f"Salvo: {nome} como {tipo}")

cap.release()
cv2.destroyAllWindows()