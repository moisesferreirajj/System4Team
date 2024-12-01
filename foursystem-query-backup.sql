-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.32-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;system4teamsystem4team
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para system4team
CREATE DATABASE IF NOT EXISTS `system4team` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `system4team`;

-- Copiando estrutura para tabela system4team.cargos
CREATE TABLE IF NOT EXISTS `cargos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.cargos: ~5 rows (aproximadamente)
INSERT IGNORE INTO `cargos` (`id`, `nome`) VALUES
	(1, 'Tech-Lead'),
	(2, 'Senior'),
	(3, 'CEO'),
	(4, 'CTO'),
	(5, 'Cliente');

-- Copiando estrutura para tabela system4team.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf` (`cpf`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.clientes: ~0 rows (aproximadamente)
INSERT IGNORE INTO `clientes` (`id`, `nome`, `cpf`, `endereco`, `telefone`, `email`, `id_empresa`) VALUES
	(1, 'DeideCosta', '11122233344', 'Inexistente, 66', '4791270100', 'system@gmail.com', 1);

-- Copiando estrutura para tabela system4team.codigos_recuperacao
CREATE TABLE IF NOT EXISTS `codigos_recuperacao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `codigo` varchar(6) NOT NULL,
  `data_envio` datetime DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `usado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `codigos_recuperacao_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.codigos_recuperacao: ~0 rows (aproximadamente)

-- Copiando estrutura para tabela system4team.despesas
CREATE TABLE IF NOT EXISTS `despesas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_empresa` int(11) DEFAULT NULL,
  `valor` decimal(10,2) NOT NULL,
  `data_despesa` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `despesas_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.despesas: ~2 rows (aproximadamente)
INSERT IGNORE INTO `despesas` (`id`, `id_empresa`, `valor`, `data_despesa`) VALUES
	(1, 1, 1500.00, '2024-11-22 20:49:36'),
	(2, 1, 1000.00, '2024-09-22 20:54:26');

-- Copiando estrutura para tabela system4team.empresas
CREATE TABLE IF NOT EXISTS `empresas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cnpj` varchar(14) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnpj` (`cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.empresas: ~0 rows (aproximadamente)
INSERT IGNORE INTO `empresas` (`id`, `nome`, `cnpj`, `endereco`, `telefone`, `email`) VALUES
	(1, 'SystemForTeam', '11111111111111', 'Rua Inexistente 147, Joinville SC', '47991270120', 'nubmoises321@gmail.com');

-- Copiando estrutura para tabela system4team.funcionarios
CREATE TABLE IF NOT EXISTS `funcionarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cargo` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cargo` (`cargo`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `funcionarios_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `cargos` (`id`),
  CONSTRAINT `funcionarios_ibfk_2` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.funcionarios: ~0 rows (aproximadamente)
INSERT IGNORE INTO `funcionarios` (`id`, `nome`, `cargo`, `email`, `telefone`, `id_empresa`) VALUES
	(1, 'Moises João Ferreira', 1, 'nubmoises@gmail.com', '47991270120', 1);

-- Copiando estrutura para tabela system4team.pedidos
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `id_produto` int(11) NOT NULL,
  `id_funcionario` int(11) DEFAULT NULL,
  `quantidade` int(11) NOT NULL,
  `id_venda` int(11) NOT NULL,
  `data_pedido` datetime DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  `finalizado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_produto` (`id_produto`),
  KEY `id_funcionario` (`id_funcionario`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id`),
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionarios` (`id`),
  CONSTRAINT `pedidos_ibfk_4` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.pedidos: ~6 rows (aproximadamente)
INSERT IGNORE INTO `pedidos` (`id`, `id_cliente`, `id_produto`, `id_funcionario`, `quantidade`, `id_venda`, `data_pedido`, `id_empresa`, `finalizado`) VALUES
	(1, 1, 2, 1, 1, 1, '2024-11-21 14:27:58', 1, 1),
	(2, 1, 1, 1, 1, 1, '2024-11-21 14:27:58', 1, 1),
	(3, 1, 2, 1, 1, 1, '2024-09-21 14:27:58', 1, 1),
	(4, 1, 3, 1, 1, 2, '2024-10-26 16:00:59', 1, 0),
	(5, 1, 2, 1, 2, 3, '2024-10-26 16:00:59', 1, 0),
	(6, 1, 2, 1, 5, 4, '2024-11-28 19:27:28', 1, 0),
  (7, 1, 1, 1, 9, 2, '2024-12-01 01:06:25', 1, 1);

-- Copiando estrutura para tabela system4team.produtos
CREATE TABLE IF NOT EXISTS `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `preco` decimal(10,2) NOT NULL,
  `quantidade` int(11) NOT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `produtos_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.produtos: ~2 rows (aproximadamente)
INSERT IGNORE INTO `produtos` (`id`, `nome`, `descricao`, `preco`, `quantidade`, `id_empresa`) VALUES
	(1, 'Site', 'Um site desenvolvido', 1000.00, 1, 1),
	(2, 'Yohan', 'Corpo do yohan desovado', 2000.00, 1, 1),
	(3, 'Aplicativo', 'Aplicativo mobile desenvolvido', 3500.00, 1, 1);

-- Copiando estrutura para tabela system4team.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `cargo` int(11) DEFAULT NULL,
  `imagem` varchar(255) DEFAULT NULL,
  `id_funcionario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `cargo` (`cargo`),
  KEY `id_funcionario` (`id_funcionario`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `cargos` (`id`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Copiando dados para a tabela system4team.usuarios: ~9 rows (aproximadamente)
INSERT IGNORE INTO `usuarios` (`id`, `usuario`, `senha`, `email`, `cargo`, `imagem`, `id_funcionario`) VALUES
	(1, 'moises', '$2b$12$COoAGcMBJMW19TkFhOvHEOu82G/XbPp/PH03Nllwmp/Hz4XiaSwTm', 'parameuamigosun4@gmail.com', 1, 'moises.jfif', 1),
	(2, 'igor', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'igor@gmail.com', 2, 'igor2.jfif', NULL),
	(3, 'mark', '$2b$12$m2.E4QS0lr/RVqopPhqrnecTNwGtHF.dCBij2naH3307IrJ1TM4iK', 'markstolfi2@gmail.com', 2, NULL, NULL),
	(4, 'yohan', '$2b$12$wouY5sgcHGuw9b7oKGJ9aurC/iYBkA6f53GK5DUSC1d00BlY4p9cS', 'yohan@gmail.com', 4, NULL, NULL),
	(5, 'senhorinha', '$2b$12$R4AFjGq1m/p6fqUSY2hIxekvKKrNHOyUIGizntzEfzjMpFewaBJ/e', 'marciosenhorinha@gmail.com', NULL, NULL, NULL),
	(13, 'Moises Ferreira', '$2b$12$WxhkPj5xkA1.OMmBSyPTdeUbuvCQ0cj7WLFsikBPKPHjNix68Ngpq', 'nubmoises321@gmail.com', NULL, 'moises.jfif', NULL),
	(14, 'NataliAlberton', '$2b$12$lPh1kDvrR3eUWFiX8X1oWO.6GwUbzR30IlyZHCukeFSxfQx7KvuQC', 'alberton.natali@gmail.com', NULL, NULL, NULL),
	(15, 'mark12', '$2b$12$rOt8bTKPreCQ51uXUWmD8ex9rIoNBSM.xJ25OZ0r23FKBcLuXtQtS', 'markstolf2i2@gmail.com', 3, NULL, NULL),
	(17, 'Moiseszinho', '$2b$12$ByiOckYHvBxZ2EzDSjumMet5SVGy.duo.SHMOxtA3mwsM95jwoRJy', 'nubmoises@gmail.com', 1, 'moises.jfif', NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;