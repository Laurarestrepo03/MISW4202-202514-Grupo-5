--Tabla pedidos que será auditada
CREATE TABLE pedidos (pedido_id SERIAL PRIMARY KEY,nombre VARCHAR(100) NOT NULL,cantidad INT NOT NULL,precio FLOAT NOT NULL,fecha_pedido TIMESTAMP);
GRANT ALL PRIVILEGES ON TABLE pedidos TO medy_supply_app;

--Tabla de auditoria, en la que se guardarán todas las operaciones de inserción, actualización o eliminación de registros de la tabla pedidos
CREATE TABLE audit_log (id SERIAL PRIMARY KEY, pedido_id INT, accion VARCHAR(100), usuario VARCHAR(200), message VARCHAR(200), fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
GRANT ALL PRIVILEGES ON TABLE audit_log TO medy_supply_app;

--Función que se ejecuta con el trigger. 
--Inserta un registro en la tabla de auditoria especificando el tipo de operación que se realizó, el usuario que la realizó y el id del pedido
CREATE OR REPLACE FUNCTION audit_log_pedidos_fn()
RETURNS TRIGGER AS $$
BEGIN
 INSERT INTO audit_log (pedido_id, accion, usuario, message)
 VALUES (NEW.pedido_id, TG_OP, CURRENT_USER, 'El usuario '||CURRENT_USER||' ha realizado una operaciOn de '||TG_OP||' sobre el pedido con id '||NEW.pedido_id||' en la tabla '||TG_TABLE_NAME);
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger que se ejecuta con cualquier tipo de acción INSERT, UPDATE, DELETE sobre la tabla de pedidos
CREATE TRIGGER pedidos_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON pedidos
FOR EACH ROW
EXECUTE FUNCTION audit_log_pedidos_fn();