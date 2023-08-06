from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, inspect, select
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()

class Cliente(Base): 
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    conta = relationship("Conta", back_populates="cliente")

    def __repr__(self): 
        return f"Cliente(id={self.id}), nome={self.nome}"

class Conta(Base): 
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    saldo = Column(Integer)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self): 
        return f"Conta(id={self.id}), num={self.num}"

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspector_engine = inspect(engine)
print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)

with Session(engine) as session: 
    joao = Cliente(nome="João", cpf = "João da Silva", endereco = "João da Silva", conta = [Conta(tipo= "corrente", agencia= "corrente", num= 1, saldo= 15)]
    )

session.add_all([joao])
session.commit()


stmt = select(Cliente).where(Cliente.nome.in_(['João']))
print(stmt)

for cliente in session.scalars(stmt): 
    print(cliente)
    print(cliente.nome)