import os

from web.app import app
import usuarios

def ensure_admin():
    admin_login = 'admin001'
    if not usuarios.buscar_usuario_por_login(admin_login):
        usuarios.cadastrar_usuario(
            nome='Admin User',
            login=admin_login,
            senha='adminpass',
            email='admin@example.com',
            setor='recepção'
        )
    return admin_login, 'adminpass'

def test_routes():
    client = app.test_client()
    admin_login, admin_pass = ensure_admin()
    login_resp = client.post('/login', data={'login': admin_login, 'senha': admin_pass}, follow_redirects=True)
    assert login_resp.status_code == 200, f'Login failed with status {login_resp.status_code}'
    resp = client.get('/usuarios/novo')
    assert resp.status_code == 200, f'GET /usuarios/novo returned {resp.status_code}'
    data = {
        'nome': 'Dr Teste',
        'login': '12345678900',
        'email': 'dr.teste@example.com',
        'senha': '123456',
        'setor': 'médico',
        'especialidade': 'Cardiologia'
    }
    resp = client.post('/usuarios/novo', data=data, follow_redirects=True)
    assert resp.status_code == 200, f'POST /usuarios/novo returned {resp.status_code}'
    user = usuarios.buscar_usuario_por_login('12345678900')
    assert user is not None, 'User not found after registration'
    assert user.get('especialidade') == 'Cardiologia', 'Specialty not saved'
    print('All tests passed')

if __name__ == '__main__':
    test_routes()
