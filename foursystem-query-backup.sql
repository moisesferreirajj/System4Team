-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.22-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando dados para a tabela system4team.cargos: ~5 rows (aproximadamente)
INSERT IGNORE INTO `cargos` (`id`, `nome`) VALUES
	(1, 'Tech-Lead'),
	(2, 'Senior'),
	(3, 'CEO'),
	(4, 'CTO'),
	(5, 'Cliente');

-- Copiando dados para a tabela system4team.clientes: ~1 rows (aproximadamente)
INSERT IGNORE INTO `clientes` (`id`, `nome`, `cpf`, `endereco`, `telefone`, `email`, `id_empresa`) VALUES
	(1, 'DeideCosta', '11122233344', 'Inexistente, 66', '4791270100', 'system@gmail.com', 1);

-- Copiando dados para a tabela system4team.codigos_recuperacao: ~0 rows (aproximadamente)

-- Copiando dados para a tabela system4team.empresas: ~1 rows (aproximadamente)
INSERT IGNORE INTO `empresas` (`id`, `nome`, `cnpj`, `endereco`, `telefone`, `email`) VALUES
	(1, 'SystemForTeam', '11111111111111', 'Rua Inexistente 147, Joinville SC', '47991270120', 'nubmoises321@gmail.com');

-- Copiando dados para a tabela system4team.funcionarios: ~1 rows (aproximadamente)
INSERT IGNORE INTO `funcionarios` (`id`, `nome`, `cargo`, `email`, `telefone`, `id_empresa`) VALUES
	(1, 'Moises João Ferreira', 1, 'nubmoises@gmail.com', '47991270120', 1);

-- Copiando dados para a tabela system4team.pedidos: ~1 rows (aproximadamente)
INSERT IGNORE INTO `pedidos` (`id`, `id_cliente`, `id_produto`, `id_funcionario`, `quantidade`, `id_venda`, `data_pedido`, `id_empresa`, `finalizado`) VALUES
	(1, 1, 2, 1, 1, 1, '2024-11-21 14:27:58', 1, 1);

-- Copiando dados para a tabela system4team.produtos: ~2 rows (aproximadamente)
INSERT IGNORE INTO `produtos` (`id`, `nome`, `descricao`, `preco`, `quantidade`, `id_empresa`) VALUES
	(1, 'Site', 'Um site desenvolvido', 1000.00, 1, 1),
	(2, 'Yohan', 'Corpo do yohan desovado', 2000.00, 1, 1);

-- Copiando dados para a tabela system4team.usuarios: ~8 rows (aproximadamente)
INSERT IGNORE INTO `usuarios` (`id`, `usuario`, `senha`, `email`, `cargo`, `imagem`, `id_funcionario`) VALUES
	(1, 'moises', '$2b$12$COoAGcMBJMW19TkFhOvHEOu82G/XbPp/PH03Nllwmp/Hz4XiaSwTm', 'parameuamigosun4@gmail.com', 1, 'moises.jfif', 1),
	(2, 'igor', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'igor@gmail.com', 2, NULL, NULL),
	(3, 'mark', '$2b$12$m2.E4QS0lr/RVqopPhqrnecTNwGtHF.dCBij2naH3307IrJ1TM4iK', 'markstolfi2@gmail.com', 2, NULL, NULL),
	(4, 'yohan', '$2b$12$wouY5sgcHGuw9b7oKGJ9aurC/iYBkA6f53GK5DUSC1d00BlY4p9cS', 'yohan@gmail.com', 4, NULL, NULL),
	(5, 'senhorinha', '$2b$12$R4AFjGq1m/p6fqUSY2hIxekvKKrNHOyUIGizntzEfzjMpFewaBJ/e', 'marciosenhorinha@gmail.com', NULL, NULL, NULL),
	(13, 'Moises Ferreira', '$2b$12$WxhkPj5xkA1.OMmBSyPTdeUbuvCQ0cj7WLFsikBPKPHjNix68Ngpq', 'nubmoises321@gmail.com', NULL, 'moises.jfif', NULL),
	(14, 'NataliAlberton', '$2b$12$lPh1kDvrR3eUWFiX8X1oWO.6GwUbzR30IlyZHCukeFSxfQx7KvuQC', 'alberton.natali@gmail.com', NULL, NULL, NULL),
	(15, 'mark12', '$2b$12$rOt8bTKPreCQ51uXUWmD8ex9rIoNBSM.xJ25OZ0r23FKBcLuXtQtS', 'markstolf2i2@gmail.com', 3, NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
