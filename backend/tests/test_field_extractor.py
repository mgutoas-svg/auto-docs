import pytest
from app.services.field_extractor import FieldExtractor


class TestFieldExtractor:

    def test_extract_single_field(self):
        """Testa extração de um único campo"""
        content = "Olá {nome}"
        fields = FieldExtractor.extract_fields(content)

        assert len(fields) == 1
        assert fields[0]["name"] == "nome"
        assert fields[0]["field_type"] == "text"
        assert fields[0]["required"] == True

    def test_extract_multiple_fields(self):
        """Testa extração de múltiplos campos"""
        content = "Meu nome é {nome}, nascido em {data_nascimento}, email: {email}"
        fields = FieldExtractor.extract_fields(content)

        assert len(fields) == 3
        assert fields[0]["name"] == "nome"
        assert fields[1]["name"] == "data_nascimento"
        assert fields[2]["name"] == "email"

    def test_extract_duplicate_fields(self):
        """Testa que campos duplicados aparecem uma só vez"""
        content = "O nome é {nome} e o sobrenome também é {nome}"
        fields = FieldExtractor.extract_fields(content)

        assert len(fields) == 1
        assert fields[0]["name"] == "nome"

    def test_infer_date_field_type(self):
        """Testa inferência de tipo data"""
        content = "Data: {data}"
        fields = FieldExtractor.extract_fields(content)

        assert fields[0]["field_type"] == "date"

    def test_infer_email_field_type(self):
        """Testa inferência de tipo email"""
        content = "Email: {email}"
        fields = FieldExtractor.extract_fields(content)

        assert fields[0]["field_type"] == "email"

    def test_validate_required_fields(self):
        """Testa validação de campos obrigatórios"""
        content = "Nome: {nome}, Data: {data}"
        data = {"nome": "João"}

        is_valid, msg = FieldExtractor.validate_fields(content, data)

        assert is_valid == False
        assert "data" in msg

    def test_validate_all_fields_filled(self):
        """Testa validação quando todos os campos estão preenchidos"""
        content = "Nome: {nome}, Data: {data}"
        data = {"nome": "João", "data": "01/01/2024"}

        is_valid, msg = FieldExtractor.validate_fields(content, data)

        assert is_valid == True
        assert msg == ""

    def test_replace_fields(self):
        """Testa substituição de campos"""
        content = "Olá {nome}, bem-vindo!"
        data = {"nome": "João"}

        result = FieldExtractor.replace_fields(content, data)

        assert result == "Olá João, bem-vindo!"
        assert "{nome}" not in result

    def test_replace_multiple_fields(self):
        """Testa substituição de múltiplos campos"""
        content = "{saudacao} {nome}, sua data é {data}"
        data = {"saudacao": "Olá", "nome": "João", "data": "01/01/2024"}

        result = FieldExtractor.replace_fields(content, data)

        assert result == "Olá João, sua data é 01/01/2024"

    def test_has_unreplaced_fields(self):
        """Testa detecção de campos não substituídos"""
        content_with_fields = "Olá {nome}"
        content_without_fields = "Olá João"

        assert FieldExtractor.has_unreplaced_fields(content_with_fields) == True
        assert FieldExtractor.has_unreplaced_fields(content_without_fields) == False

    def test_get_unreplaced_field_names(self):
        """Testa obtenção de nomes de campos não substituídos"""
        content = "Olá {nome}, sua data é {data_inicio}"

        unreplaced = FieldExtractor.get_unreplaced_field_names(content)

        assert "nome" in unreplaced
        assert "data_inicio" in unreplaced
        assert len(unreplaced) == 2
