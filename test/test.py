# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.result import TestFailure

clk_period = 100 # Ciclo de reloj de 100 ns.

@cocotb.test()
async def test_counter_reset(dut):
    """Prueba para ver que el contador se resetea correctamente."""
    dut._log.info("Iniciando TB.")

    #Configurando el reloj de señal.
    clock = Clock(dut.clk, clk_period, unit="ns")
    cocotb.start_soon(clock.start())

    #Simulamos las señales que queremos excitar.
    #Reset activo en bajo.
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)

    #Liberar el reset
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    #Poniendo un assertion para ver si se reseteó correctamente.
    #if dut.c.value.interger ! = 0:
    #    raise TestFailure(f"El contador no se reseteó correctamente. Valor = {dut.c.value}")
    #else
    dut._log.info("Reset funcionando correctamente.")

@cocotb.test()
async def test_counter_enable_260(dut):
    """Prueba que el contador incremente cuando enable = 1."""
    dut._log.info("Iniciando Tb: enable.")

    #Configurando el reloj de señal.
    clock = Clock(dut.clk, clk_period, unit="ns")
    cocotb.start_soon(clock.start())

    #Reset.
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    #Habilitar el contador.
    dut.ui.in_value = 1
    await ClockCycles(dut.clk, 260)

    expected = 4
    observed = dut.c.value.integer

    dut._log.info(f"Valor esperado: {expected}, observado: {observed}.")

    if observed != expected:
        raise TestFailure(f"Error en conteo con enable = 1. Esperador={expected}, Observado={observed}.")

    dut._log.info("Enable funcionando correctamente.")


@cocotb.test()
async def test_counter_enable(dut):
    """Prueba que el contador incremente cuando enable = 1."""
    dut._log.info("Iniciando Tb: enable.")

    #Configurando el reloj de señal.
    clock = Clock(dut.clk, clk_period, unit="ns")
    cocotb.start_soon(clock.start())

    #Reset.
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    #Habilitar el contador.
    dut.ui.in_value = 1
    await ClockCycles(dut.clk, 5)

    expected = 4
    observed = dut.c.value.integer

    dut._log.info(f"Valor esperado: {expected}, observado: {observed}.")

    dut._log.info("Enable funcionando correctamente.")



@cocotb.test()
async def test_counter_disable(dut):
    """Prueba que el contador no cambie cuando enable = 0."""
    dut._log.info("Iniciando TB: disable.")
    
    
    #Configurando el reloj de señal.
    clock = Clock(dut.clk, clk_period, unit="ns")
    cocotb.start_soon(clock.start())

    #Reset.
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    #Contar 3 ciclos con enable = 1.
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 4)

    prev_value = dut.c.value.integer + 1

    #Deshabilitar contador.
    dut.ui._in.value = 0
    await ClockCycles(dut.clk, 4)

    observed = dut.c.value.integer

    dut._log.info(f"Valor previo: {prev_value}, observando después del disable: {observed}.")

    dut._log.info("Enable funcionando correctamente.")
