CREATE TABLE dono (
	id	 BIGSERIAL,
	nome	 VARCHAR(100) NOT NULL,
	nif	 VARCHAR(9),
	telefone VARCHAR(9) NOT NULL,
	email	 VARCHAR(255),
	PRIMARY KEY(id)
);

CREATE TABLE animal (
	id		 BIGSERIAL,
	nome		 VARCHAR(100) NOT NULL,
	especie	 VARCHAR(50) NOT NULL,
	raca		 VARCHAR(50),
	data_nascimento DATE,
	foto		VARCHAR(100),
	dono_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE consulta (
	id		 BIGSERIAL,
	data_hora	 TIMESTAMP NOT NULL,
	motivo	 VARCHAR(255),
	observacoes	 VARCHAR(255),
	veterinario_id BIGINT NOT NULL,
	animal_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE veterinario (
	id			 BIGSERIAL,
	nome		 VARCHAR(100) NOT NULL,
	celula_profissional VARCHAR(20) NOT NULL,
	especialidade	 VARCHAR(100),
	telefone		 VARCHAR(9) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE medicamento (
	id	 BIGSERIAL,
	nome	 VARCHAR(100) NOT NULL,
	fabricante VARCHAR(100),
	dose	 VARCHAR(50),
	PRIMARY KEY(id)
);

CREATE TABLE detalheconsulta (
	id		 BIGSERIAL,
	quantidade	 INTEGER NOT NULL DEFAULT 1,
	preco		 NUMERIC(10, 2) NOT NULL,
	notas		 VARCHAR(255),
	medicamento_id BIGINT,
	servico_id	 BIGINT,
	consulta_id	 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE servico (
	id	 BIGSERIAL,
	servico VARCHAR(100) NOT NULL,
	preco	 NUMERIC(10, 2) NOT NULL,
	PRIMARY KEY(id)
);

ALTER TABLE dono ADD CONSTRAINT NIF_9 CHECK (nif ~ '^[0-9]{9}$');
ALTER TABLE dono ADD CONSTRAINT TLF_9 CHECK (telefone ~ '^[0-9]{9}$');
ALTER TABLE animal ADD CONSTRAINT animal_fk1 FOREIGN KEY (dono_id) REFERENCES dono(id);
ALTER TABLE consulta ADD CONSTRAINT consulta_fk1 FOREIGN KEY (veterinario_id) REFERENCES veterinario(id);
ALTER TABLE consulta ADD CONSTRAINT consulta_fk2 FOREIGN KEY (animal_id) REFERENCES animal(id);
ALTER TABLE veterinario ADD UNIQUE (celula_profissional);
ALTER TABLE detalheconsulta ADD CONSTRAINT detalheconsulta_fk1 FOREIGN KEY (medicamento_id) REFERENCES medicamento(id);
ALTER TABLE detalheconsulta ADD CONSTRAINT detalheconsulta_fk2 FOREIGN KEY (servico_id) REFERENCES servico(id);
ALTER TABLE detalheconsulta ADD CONSTRAINT detalheconsulta_fk3 FOREIGN KEY (consulta_id) REFERENCES consulta(id);