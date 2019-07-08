from smnp.error.function import FunctionNotFoundException, MethodNotFoundException, IllegalFunctionInvocationException
from smnp.error.runtime import RuntimeException
from smnp.library.model import types
from smnp.runtime.evaluators.function import BodyEvaluator


class Environment():
    def __init__(self, scopes, functions, methods):
        self.scopes = scopes
        self.functions = functions
        self.methods = methods
        self.customFunctions = []
        self.customMethods = []

    def invokeMethod(self, object, name, args):
        builtinMethodResult = self._invokeBuiltinMethod(object, name, args)
        if builtinMethodResult[0]:
            return builtinMethodResult[1]

        customMethodResult = self._invokeCustomMethod(object, name, args)
        if customMethodResult[0]:
            return customMethodResult[1]

        raise MethodNotFoundException(object.type, name)

    def _invokeBuiltinMethod(self, object, name, args):
        for method in self.methods:
            if method.name == name:
                ret = method.call(self, [object, *args])
                if ret is not None:
                    return (True, ret)

        return (False, None)

    def _invokeCustomMethod(self, object, name, args):
        for function in self.customMethods:
            if function.name == name:
                signatureCheckresult = function.signature.check(args)
                if signatureCheckresult[0]:
                    self.scopes.append({argName: argValue for argName, argValue in zip(function.arguments, args)})
                    result = BodyEvaluator.evaluate(function.body, self).value  # TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    self.scopes.pop(-1)
                    return (True, result)
                raise IllegalFunctionInvocationException(f"{function.name}{function.signature.string}",
                                                         f"{name}{types(args)}")
        return (False, None)

    def invokeFunction(self, name, args):
        builtinFunctionResult = self._invokeBuiltinFunction(name, args)
        if builtinFunctionResult[0]:
            return builtinFunctionResult[1]

        customFunctionResult = self._invokeCustomFunction(name, args)
        if customFunctionResult[0]:
            return customFunctionResult[1]

        raise FunctionNotFoundException(name)

    def _invokeBuiltinFunction(self, name, args):
        for function in self.functions:
            if function.name == name:
                ret = function.call(self, args)
                if ret is not None:
                    return (True, ret)

        return (False, None)

    def _invokeCustomFunction(self, name, args):
        for function in self.customFunctions:
            if function.name == name:
                signatureCheckresult = function.signature.check(args)
                if signatureCheckresult[0]:
                    self.scopes.append({ argName: argValue for argName, argValue in zip(function.arguments, args) })
                    result = BodyEvaluator.evaluate(function.body, self).value #TODO check if it isn't necessary to verify 'result' attr of EvaluatioNResult
                    self.scopes.pop(-1)
                    return (True, result)
                raise IllegalFunctionInvocationException(f"{function.name}{function.signature.string}", f"{name}{types(args)}")
        return (False, None)

    def addCustomFunction(self, name, signature, arguments, body):
        self.customFunctions.append(CustomFunction(name, signature, arguments, body))

    def findVariable(self, name, type=None, pos=None):
        for scope in reversed(self.scopes):
            if name in scope:
                value = scope[name]
                if type is not None:
                    if isinstance(value, type):
                        return value
                else:
                    return value
        raise RuntimeException(f"Variable '{name}' is not declared" + (
            "" if type is None else f" (expected type: {type})"), pos)

    def findVariableScope(self, name, type=None):
        for scope in reversed(self.scopes):
            if name in scope:
                if type is not None:
                    if isinstance(scope[name], type):
                        return scope
                else:
                    return scope

    def scopesToString(self):
        return "Scopes:\n" + ("\n".join([ f"  [{i}]: {scope}" for i, scope in enumerate(self.scopes) ]))

    def functionsToString(self):
        return "Functions:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.functions ]))

    def customFunctionsToString(self):
        return "Custom Functions:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.customFunctions ]))

    def methodsToString(self):
        return "Methods:\n" + ("\n".join([f"  {function.name}(...)" for function in self.methods]))

    def customMethodsToString(self):
        return "Custom Methods:\n" + ("\n".join([ f"  {function.name}(...)" for function in self.customMethods ]))


    def __str__(self):
        return self.scopesToString() + self.functionsToString() + self.methodsToString() + self.customFunctionsToString() + self.customMethodsToString()

    def __repr__(self):
        return self.__str__()


class CustomFunction:
    def __init__(self, name, signature, arguments, body):
        self.name = name
        self.signature = signature
        self.arguments = arguments
        self.body = body