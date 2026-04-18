-- 1. Inserir Donos (10 clientes)
INSERT INTO dono (nome, nif, telefone, email) VALUES
('Rui Silva', '212345678', '912345678', 'rui.silva@email.com'),
('Ana Costa', '298765432', '965432198', 'ana.costa@email.pt'),
('Miguel Santos', '255666777', '933444555', 'miguel.santos@email.com'),
('Carla Mendes', '244111222', '911222333', 'carla.m@hotmail.com'),
('Tiago Oliveira', '211999888', '966777888', 'tiago.oliveira@empresa.pt'),
('Sónia Pereira', '233444555', '922111333', 'sonia.p@sapo.pt'),
('Bruno Fernandes', '288777666', '933999111', 'bruno.fernandes@email.com'),
('Diana Martins', '222333444', '911555777', NULL),
('João Teixeira', '277888999', '966222444', 'joao.teixeira@email.com'),
('Rita Carvalho', '266555444', '933111222', 'rita_carvalho89@gmail.com');

-- 2. Inserir Animais (15 animais - alguns donos têm mais de um)
INSERT INTO animal (nome, especie, raca, data_nascimento, dono_id) VALUES
('Bobby', 'Cão', 'Rafeiro', '2018-05-10', 1),          
('Luna', 'Gato', 'Siamês', '2020-08-22', 2),          
('Rex', 'Cão', 'Pastor Alemão', '2019-11-05', 2),     
('Mia', 'Gato', 'Persa', '2022-01-15', 3),
('Bolinhas', 'Coelho', 'Anão', '2023-03-10', 4),
('Thor', 'Cão', 'Bulldog Francês', '2021-07-30', 5),
('Simba', 'Gato', 'Europeu Comum', '2017-04-12', 6),
('Nala', 'Gato', 'Europeu Comum', '2017-04-12', 6),
('Max', 'Cão', 'Golden Retriever', '2020-12-01', 7),
('Kira', 'Cão', 'Husky', '2019-02-18', 8),
('Tareco', 'Gato', 'Rafeiro', '2015-09-09', 9),
('Pipoca', 'Cão', 'Poodle', '2022-11-20', 10),
('Bethoven', 'Cão', 'São Bernardo', '2018-01-05', 10),
('Félix', 'Gato', 'Maine Coon', '2021-06-15', 1),
('Pepe', 'Pássaro', 'Canário', '2023-01-10', 5);

-- 3. Inserir Veterinários (5 profissionais)
INSERT INTO veterinario (nome, celula_profissional, especialidade, telefone) VALUES
('Dra. Sofia Almeida', 'VET-1234', 'Cirurgia', '911111111'),
('Dr. João Pedro', 'VET-5678', 'Clínica Geral', '922222222'),
('Dra. Marta Sousa', 'VET-9012', 'Dermatologia e Alergias', '933333333'),
('Dr. Carlos Rocha', 'VET-3456', 'Animais Exóticos', '966666666'),
('Dra. Inês Lima', 'VET-7890', 'Medicina Interna', '922555555');

-- 4. Inserir Serviços (10 serviços diversos)
INSERT INTO servico (servico, preco) VALUES
('Consulta de Rotina', 35.00),
('Vacinação Anual', 25.00),
('Desparasitação Interna', 15.00),
('Colocação de Microchip', 20.00),
('Raio-X', 45.00),
('Ecografia Abdominal', 60.00),
('Limpeza Dentária', 85.00),
('Internamento (Dia)', 50.00),
('Exame de Sangue (Hemograma)', 40.00),
('Corte de Unhas', 10.00);

-- 5. Inserir Medicamentos (10 medicamentos)
INSERT INTO medicamento (nome, fabricante, dose) VALUES
('Bravecto', 'MSD Animal Health', '1 comprimido'),
('Milbemax', 'Elanco', '1 comprimido'),
('Meloxicam', 'Vetoquinol', '1.5mg/ml gota'),
('Vacina Nobivac DHPPI', 'MSD Animal Health', '1 dose'),
('Vacina Felv', 'Zoetis', '1 dose'),
('Synulox 50mg', 'Zoetis', '1 comprimido/12h'),
('Cerenia', 'Zoetis', '1 comprimido'),
('Apoquel 16mg', 'Zoetis', '1 comprimido/dia'),
('Panacur Pasta', 'MSD', '1 seringa'),
('Soro Fisiológico', 'B. Braun', '250ml IV');

-- 6. Inserir Consultas (10 consultas históricas e recentes)
INSERT INTO consulta (data_hora, motivo, observacoes, veterinario_id, animal_id) VALUES
('2023-10-25 10:00:00', 'Vacinação Anual', 'Animal saudável, peso normal.', 2, 1),
('2023-10-25 11:30:00', 'Comichão e queda de pelo', 'Suspeita de dermatite alérgica alimentar.', 3, 2),
('2023-10-26 15:00:00', 'Claudicação pata traseira', 'Começou ontem após salto. Dor à palpação.', 1, 3),
('2023-10-27 09:30:00', 'Check-up anual', 'Tudo regular.', 2, 4),
('2023-10-27 11:00:00', 'Dentes a crescer muito', 'Dentes desgastados com sucesso.', 4, 5),
('2023-10-28 14:00:00', 'Vómitos repetidos', 'Apresentou vómitos desde a manhã. Feito raio-X.', 5, 6),
('2023-10-28 16:30:00', 'Vacinação felina', 'Veio com o irmão (Nala). Tudo ok.', 2, 7),
('2023-10-28 16:45:00', 'Vacinação felina', 'Veio com o irmão (Simba). Tudo ok.', 2, 8),
('2023-10-29 10:00:00', 'Limpeza dentária', 'Gengivite acentuada. Extraído um dente.', 1, 11),
('2023-10-30 18:00:00', 'Corte de unhas', 'Apenas serviço de estética.', 2, 15);

-- 7. Inserir Detalhes das Consultas (Faturação)
-- C1: Bobby (Vacina + Desparasitante)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 25.00, 'Serviço vacinação', NULL, 2, 1),
(1, 15.00, 'Nobivac', 4, NULL, 1),
(1, 32.00, 'Bravecto prevenção', 1, NULL, 1);

-- C2: Luna (Dermatologia)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 35.00, 'Consulta de especialidade', NULL, 1, 2),
(1, 45.00, 'Apoquel para alergia', 8, NULL, 2);

-- C3: Rex (Ortopedia)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 35.00, 'Consulta geral', NULL, 1, 3),
(1, 45.00, 'Raio-X membro pélvico', NULL, 5, 3),
(1, 12.50, 'Meloxicam gotas', 3, NULL, 3);

-- C4: Mia (Check-up)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 35.00, 'Consulta rotina', NULL, 1, 4);

-- C5: Bolinhas (Exótico)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 35.00, 'Consulta Exóticos', NULL, 1, 5);

-- C6: Thor (Urgência Vómitos)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 35.00, 'Consulta rotina', NULL, 1, 6),
(1, 45.00, 'Raio-X Abdominal', NULL, 5, 6),
(1, 40.00, 'Análise de sangue', NULL, 9, 6),
(1, 18.00, 'Anti-emético (Cerenia)', 7, NULL, 6);

-- C7 & C8: Simba e Nala (Vacinas conjuntas)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 25.00, 'Vacinação', NULL, 2, 7),
(1, 15.00, 'Vacina Felv', 5, NULL, 7),
(1, 25.00, 'Vacinação', NULL, 2, 8),
(1, 15.00, 'Vacina Felv', 5, NULL, 8);

-- C9: Tareco (Dentária)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 85.00, 'Limpeza c/ Anestesia', NULL, 7, 9),
(1, 15.00, 'Antibiótico pós-operatório (Synulox)', 6, NULL, 9);

-- C10: Pepe (Pássaro, unhas)
INSERT INTO detalheconsulta (quantidade, preco, notas, medicamento_id, servico_id, consulta_id) VALUES
(1, 10.00, 'Corte unhas', NULL, 10, 10);