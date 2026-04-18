# 🗄️ Documentação da Base de Dados

Esta pasta contém a definição estrutural da base de dados da Clínica Veterinária. O sistema utiliza um modelo relacional robusto, preparado não só para a gestão de pacientes, mas também para o registo clínico e de faturação.

## 🗺️ Modelo de Dados (Tabelas e Atributos)

Abaixo está a descrição detalhada de cada entidade do sistema, com base no script SQL original:

### 👤 1. Dono (Cliente)
Regista a informação de contacto e faturação dos clientes da clínica.
* **id:** Identificador único (Primary Key).
* **nome:** Nome completo do cliente (Obrigatório).
* **nif:** Número de Identificação Fiscal (Validado para ter exatamente 9 dígitos).
* **telefone:** Contacto telefónico (Validado para ter exatamente 9 dígitos, Obrigatório).
* **email:** Endereço de correio eletrónico.

### 🐾 2. Animal (Paciente)
Regista os animais que são atendidos na clínica.
* **id:** Identificador único (Primary Key).
* **nome:** Nome do animal (Obrigatório).
* **especie:** Ex: Cão, Gato, Coelho (Obrigatório).
* **raca:** Raça específica do animal.
* **data_nascimento:** Data de nascimento para cálculo de idade.
* **dono_id:** Chave estrangeira que liga o animal ao seu Dono (Relação 1:N).

### 🩺 3. Veterinário
Regista a equipa clínica.
* **id:** Identificador único (Primary Key).
* **nome:** Nome do profissional (Obrigatório).
* **celula_profissional:** Número da ordem dos médicos veterinários (Obrigatório e Único).
* **especialidade:** Ex: Cirurgia, Dermatologia, Clínica Geral.
* **telefone:** Contacto telefónico (Obrigatório).

### 📅 4. Consulta
Regista o evento central da clínica: a visita de um animal a um veterinário.
* **id:** Identificador único (Primary Key).
* **data_hora:** A data e a hora exata da marcação/realização (Obrigatório).
* **motivo:** Razão da visita (Ex: Vacinação, Claudicação).
* **observacoes:** Notas clínicas detalhadas sobre a consulta.
* **veterinario_id:** Chave estrangeira do Médico responsável (Obrigatório).
* **animal_id:** Chave estrangeira do Paciente atendido (Obrigatório).

### 💊 5. Medicamento
Catálogo de produtos e fármacos disponíveis na clínica.
* **id:** Identificador único (Primary Key).
* **nome:** Nome comercial ou princípio ativo (Obrigatório).
* **fabricante:** Marca ou laboratório.
* **dose:** Concentração ou posologia padrão (Ex: 50mg, 10ml).

### 🛠️ 6. Serviço
Catálogo de procedimentos realizados na clínica com os respetivos valores.
* **id:** Identificador único (Primary Key).
* **servico:** Descrição do serviço (Ex: Ecografia, Tosquia, Cirurgia) (Obrigatório).
* **preco:** Valor base do serviço (Obrigatório).

### 📝 7. DetalheConsulta (Itens da Consulta)
Esta é uma tabela de ligação fundamental. Permite registar múltiplos serviços ou medicamentos aplicados numa única consulta (funciona como as "linhas" de uma fatura ou relatório médico).
* **id:** Identificador único (Primary Key).
* **quantidade:** Número de unidades aplicadas/vendidas (Por defeito é 1).
* **preco:** Valor cobrado no momento (permite guardar o histórico caso o preço no catálogo de Serviços mude no futuro) (Obrigatório).
* **notas:** Observações específicas sobre a aplicação deste serviço/medicamento.
* **consulta_id:** Chave estrangeira indicando a que Consulta este detalhe pertence (Obrigatório).
* **medicamento_id:** (Opcional) Chave estrangeira caso o detalhe seja a venda/aplicação de um Medicamento.
* **servico_id:** (Opcional) Chave estrangeira caso o detalhe seja a prestação de um Serviço.


## 📜 Ficheiros Incluídos
- `vet_clinic.sql`: Script original com a criação das tabelas e constrangimentos (Constraints) de validação (como os limites de NIF e Telefone, e chaves estrangeiras) em PostgreSQL.
- `seed.sql`: Script com dados iniciais de teste.