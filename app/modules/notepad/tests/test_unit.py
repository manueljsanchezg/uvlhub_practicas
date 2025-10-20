import pytest
from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.notepad.models import Notepad
from app.modules.notepad.services import NotepadService
from app.modules.profile.models import UserProfile

@pytest.fixture
def notepad_service():
    return NotepadService()

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()
    yield test_client


def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)


def test_get_all_by_user_unit(notepad_service, test_client):
    """
    Comprueba que se obtienen las notas creadas por el usuario
    """
    
    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
    
    notepad_service.create(title="Nota 1", body="A", user_id=user.id)
    notepad_service.create(title="Nota 2", body="B", user_id=user.id)

    notes = notepad_service.get_all_by_user(user.id)
    assert len(notes) >= 2
    titles = [n.title for n in notes]
    assert "Nota 1" in titles
    assert "Nota 2" in titles

    
def test_create_notepad(test_client):
    """
    Crea un notepad y verifica su aparición en la lista.
    """
    login(test_client, "user@example.com", "test1234")

    response = test_client.post(
        "/notepad/create",
        data={"title": "Nota nueva", "body": "Contenido de prueba"},
        follow_redirects=True,
    )
    
    assert response.status_code == 200
    assert b"Notepad created successfully" in response.data or b"Nota nueva" in response.data

    logout(test_client)


def test_view_notepad(test_client):
    """
    Crea un notepad y verifica que podemos acceder al notepad.
    """
    
    login(test_client, "user@example.com", "test1234")

    response_create = test_client.post(
        "/notepad/create",
        data={"title": "Ver nota", "body": "Contenido visible"},
        follow_redirects=True
    )
    assert response_create.status_code == 200
    assert b"Ver nota" in response_create.data

    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        note = Notepad.query.filter_by(user_id=user.id, title="Ver nota").first()
        note_id = note.id

    response = test_client.get(f"/notepad/{note_id}")
    assert response.status_code == 200
    assert b"Contenido visible" in response.data

    logout(test_client)



def test_edit_notepad(test_client):
    """
    Crea un notepad y verifica que podemos editer el notepad.
    """
    
    login(test_client, "user@example.com", "test1234")

    response_create = test_client.post(
        "/notepad/create",
        data={"title": "Nota a editar", "body": "Texto inicial"},
        follow_redirects=True
    )
    assert response_create.status_code == 200
    assert b"Nota a editar" in response_create.data

    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        note = Notepad.query.filter_by(user_id=user.id, title="Nota a editar").first()
        note_id = note.id

    response_edit = test_client.post(
        f"/notepad/edit/{note_id}",
        data={"title": "Nota editada", "body": "Texto actualizado"},
        follow_redirects=True
    )
    assert response_edit.status_code == 200
    assert b"Nota editada" in response_edit.data or b"Texto actualizado" in response_edit.data

    logout(test_client)



def test_delete_notepad(test_client):
    """
    Crea un notepad y verifica que podemos borrar el notepad.
    """
    
    login(test_client, "user@example.com", "test1234")

    response_create = test_client.post(
        "/notepad/create",
        data={"title": "Nota a borrar", "body": "Contenido a eliminar"},
        follow_redirects=True
    )
    assert response_create.status_code == 200
    assert b"Nota a borrar" in response_create.data

    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        note = Notepad.query.filter_by(user_id=user.id, title="Nota a borrar").first()
        note_id = note.id

    response_delete = test_client.post(
        f"/notepad/delete/{note_id}",
        follow_redirects=True
    )
    assert response_delete.status_code == 200

    with test_client.application.app_context():
        deleted = Notepad.query.get(note_id)
        assert deleted is None

    logout(test_client)
